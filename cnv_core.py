"""
CNV prediction - core logic (no Streamlit)
==========================================
Pure functions so the app's behaviour can be unit-tested headless.

SYNTHETIC DATA - educational demonstration only. NOT for clinical use.
"""

import os
import pickle
import socket
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))

# 14 predictors, in the exact order the models were trained on
FEATURES = [
    'age', 'sex_binary', 'rupture_length_mm', 'distance_from_fovea_um',
    'foveal_involvement_binary', 'choroidal_thickness_um',
    'subretinal_hemorrhage_binary', 'baseline_cst_um',
    'outer_retinal_disruption_score', 'rpe_disruption_binary',
    'ez_integrity_percent', 'subretinal_fluid_binary',
    'intraretinal_cysts_binary', 'baseline_va_logmar',
]

# Human-readable labels
LABELS = {
    'age': 'Age',
    'sex_binary': 'Male sex',
    'rupture_length_mm': 'Rupture length',
    'distance_from_fovea_um': 'Distance from fovea',
    'foveal_involvement_binary': 'Foveal involvement',
    'choroidal_thickness_um': 'Choroidal thickness',
    'subretinal_hemorrhage_binary': 'Subretinal hemorrhage',
    'baseline_cst_um': 'Baseline CST',
    'outer_retinal_disruption_score': 'Outer retinal disruption',
    'rpe_disruption_binary': 'RPE disruption',
    'ez_integrity_percent': 'EZ integrity',
    'subretinal_fluid_binary': 'Subretinal fluid',
    'intraretinal_cysts_binary': 'Intraretinal cysts',
    'baseline_va_logmar': 'Baseline VA',
}

# Preset clinical vignettes (raw input space)
PRESETS = {
    'Low risk - peripheral rupture': dict(
        age=65, sex='Male', rupture_length_mm=1.5, distance_from_fovea_um=2500,
        foveal_involvement=False, choroidal_thickness_um=260,
        subretinal_hemorrhage=False, baseline_cst_um=270,
        outer_retinal_disruption_score=1, rpe_disruption=False,
        ez_integrity_percent=85, subretinal_fluid=False,
        intraretinal_cysts=False, baseline_va_logmar=0.3),
    'High risk - foveal rupture': dict(
        age=28, sex='Male', rupture_length_mm=6.0, distance_from_fovea_um=200,
        foveal_involvement=True, choroidal_thickness_um=300,
        subretinal_hemorrhage=True, baseline_cst_um=330,
        outer_retinal_disruption_score=3, rpe_disruption=True,
        ez_integrity_percent=20, subretinal_fluid=True,
        intraretinal_cysts=True, baseline_va_logmar=1.0),
    'Intermediate - juxtafoveal': dict(
        age=45, sex='Female', rupture_length_mm=3.2, distance_from_fovea_um=700,
        foveal_involvement=False, choroidal_thickness_um=280,
        subretinal_hemorrhage=False, baseline_cst_um=300,
        outer_retinal_disruption_score=2, rpe_disruption=False,
        ez_integrity_percent=55, subretinal_fluid=True,
        intraretinal_cysts=False, baseline_va_logmar=0.6),
}

TIMES = np.arange(0, 37, 1)  # months for survival prediction


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
def load_artifacts(base=BASE):
    """Return (rf, scaler, features, cox, cohort_df). Raises on missing files."""
    with open(os.path.join(base, 'rf_model.pkl'), 'rb') as f:
        rf = pickle.load(f)
    with open(os.path.join(base, 'scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)
    with open(os.path.join(base, 'feature_list.pkl'), 'rb') as f:
        features = pickle.load(f)
    with open(os.path.join(base, 'cox_model.pkl'), 'rb') as f:
        cox = pickle.load(f)
    cohort = pd.read_csv(os.path.join(base, 'choroidal_rupture_data.csv'))
    # Safety: the Cox path reorders by module FEATURES while the RF path uses
    # the pickled feature_list. They must describe the same columns or inputs
    # would be silently scrambled. Fail loudly if a retrain changes one only.
    if list(features) != list(FEATURES):
        raise ValueError(
            'feature_list.pkl does not match cnv_core.FEATURES; '
            f'pkl={list(features)} module={FEATURES}')
    return rf, scaler, features, cox, cohort


def inputs_to_row(d):
    """Map a raw input dict (with Yes/No-style fields) to the model feature row."""
    return {
        'age': d['age'],
        'sex_binary': 1 if d['sex'] == 'Male' else 0,
        'rupture_length_mm': d['rupture_length_mm'],
        'distance_from_fovea_um': d['distance_from_fovea_um'],
        'foveal_involvement_binary': int(bool(d['foveal_involvement'])),
        'choroidal_thickness_um': d['choroidal_thickness_um'],
        'subretinal_hemorrhage_binary': int(bool(d['subretinal_hemorrhage'])),
        'baseline_cst_um': d['baseline_cst_um'],
        'outer_retinal_disruption_score': d['outer_retinal_disruption_score'],
        'rpe_disruption_binary': int(bool(d['rpe_disruption'])),
        'ez_integrity_percent': d['ez_integrity_percent'],
        'subretinal_fluid_binary': int(bool(d['subretinal_fluid'])),
        'intraretinal_cysts_binary': int(bool(d['intraretinal_cysts'])),
        'baseline_va_logmar': d['baseline_va_logmar'],
    }


# ---------------------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------------------
def predict_risk(rf, scaler, features, row):
    """Random-forest probability of CNV development for one feature row."""
    X = pd.DataFrame([row])[features]
    Xs = scaler.transform(X)
    return float(rf.predict_proba(Xs)[0, 1])


def risk_band(p):
    if p < 0.40:
        return 'Low', '#2E8B57'
    if p < 0.70:
        return 'Medium', '#B9770E'
    return 'High', '#C0392B'


def survival_curve(cox, row, times=TIMES):
    """CNV-free survival probability over time for this patient (Cox model)."""
    sf = cox.predict_survival_function(pd.DataFrame([row])[FEATURES], times=times)
    surv = sf.iloc[:, 0].values
    return np.asarray(times, dtype=float), surv


def median_time_to_cnv(times, surv):
    """First month where CNV-free survival drops to/below 0.5, else None."""
    below = np.where(surv <= 0.5)[0]
    if len(below) == 0:
        return None
    return float(times[below[0]])


def cohort_km(cohort_df, foveal=None, times=TIMES):
    """Kaplan-Meier CNV-free survival for the cohort (or a foveal subgroup).

    Gives the population baseline the individualized Cox curve is compared
    against. `foveal=True/False` restricts to the matching subgroup; None
    uses the whole cohort.
    """
    from lifelines import KaplanMeierFitter
    df = cohort_df.copy()
    df['_t'] = df.apply(
        lambda r: r['time_to_cnv_months'] if pd.notna(r['time_to_cnv_months'])
        else r['follow_up_duration_months'], axis=1)
    df['_e'] = (df['cnv_developed'] == 'Yes').astype(int)
    if foveal is not None:
        df = df[df['foveal_involvement'] == ('Yes' if foveal else 'No')]
    kmf = KaplanMeierFitter().fit(df['_t'], df['_e'])
    surv = kmf.survival_function_at_times(times).values
    return np.asarray(times, dtype=float), np.asarray(surv, dtype=float), int(len(df))


def build_report(raw, risk, band, pct, med_t, surv36, contrib):
    """Plain-text clinical-style summary the user can download."""
    from datetime import datetime
    lines = [
        'CNV RISK ASSESSMENT  (SYNTHETIC DATA - educational, NOT for clinical use)',
        '=' * 72,
        f'Generated: {datetime.now():%Y-%m-%d %H:%M}',
        '',
        'PATIENT',
        f"  Age {raw['age']}  |  {raw['sex']}  |  baseline VA "
        f"{raw['baseline_va_logmar']:.1f} logMAR",
        f"  Rupture {raw['rupture_length_mm']:.1f} mm, "
        f"{raw['distance_from_fovea_um']} um from fovea"
        f"{', foveal involvement' if raw['foveal_involvement'] else ''}",
        '',
        'RISK',
        f'  CNV probability: {risk*100:.0f}%  ({band} band)',
        f'  Cohort percentile: {pct:.0f}th of 1000 cases',
        f"  Median time to CNV: {f'{med_t:.0f} months' if med_t is not None else 'not reached within 36 months'}",
        f'  36-month CNV-free probability: {surv36*100:.0f}%',
        '',
        'TOP INDIVIDUAL DRIVERS (vs a typical patient)',
    ]
    for c in contrib[:5]:
        if abs(c['delta']) < 1e-9:
            continue
        direction = 'raises' if c['delta'] > 0 else 'lowers'
        lines.append(f"  {c['label']}: {direction} risk by "
                     f"{abs(c['delta'])*100:.0f} pts")
    lines += ['', 'Model: random forest (AUC ~0.77) + Cox proportional hazards.',
              'Synthetic data. Educational demonstration only. NOT for clinical use.']
    return '\n'.join(lines)


def cohort_reference(cohort_df):
    """Median 'typical patient' feature row used as the explanation baseline."""
    df = _binarize_cohort(cohort_df)
    ref = {f: float(df[f].median()) for f in FEATURES}
    # keep binary/ordinal fields sensible
    for f in FEATURES:
        if f.endswith('_binary'):
            ref[f] = int(round(ref[f]))
    ref['outer_retinal_disruption_score'] = int(round(ref['outer_retinal_disruption_score']))
    return ref


def local_contributions(rf, scaler, features, row, reference):
    """
    Honest, model-based per-patient explanation.
    For each feature: hold everything else fixed, swap this feature to the
    cohort reference value, and measure how much the patient's predicted risk
    changes. Positive delta = this patient's value PUSHES RISK UP vs a typical
    patient; negative = pulls risk DOWN.
    Returns list of dicts sorted by |delta|.
    """
    base = predict_risk(rf, scaler, features, row)
    out = []
    for f in features:
        if row[f] == reference[f]:
            delta = 0.0
        else:
            cf = dict(row)
            cf[f] = reference[f]
            delta = base - predict_risk(rf, scaler, features, cf)
        out.append({'feature': f, 'label': LABELS.get(f, f), 'delta': delta})
    out.sort(key=lambda d: abs(d['delta']), reverse=True)
    return out, base


def cohort_risk_distribution(rf, scaler, features, cohort_df):
    """Predicted RF risk for every patient in the cohort (for context plot)."""
    df = _binarize_cohort(cohort_df)
    X = df[features].copy()
    valid = ~X.isnull().any(axis=1)
    X = X[valid]
    Xs = scaler.transform(X)
    return rf.predict_proba(Xs)[:, 1]


def percentile_of(value, distribution):
    return float((np.asarray(distribution) < value).mean() * 100)


def _binarize_cohort(cohort_df):
    df = cohort_df.copy()
    df['foveal_involvement_binary'] = (df['foveal_involvement'] == 'Yes').astype(int)
    df['subretinal_hemorrhage_binary'] = (df['subretinal_hemorrhage'] == 'Yes').astype(int)
    df['rpe_disruption_binary'] = (df['rpe_disruption'] == 'Yes').astype(int)
    df['subretinal_fluid_binary'] = (df['subretinal_fluid'] == 'Yes').astype(int)
    df['intraretinal_cysts_binary'] = (df['intraretinal_cysts'] == 'Yes').astype(int)
    df['sex_binary'] = (df['sex'] == 'M').astype(int)
    return df


# ---------------------------------------------------------------------------
# Networking helper (phone-share link)
# ---------------------------------------------------------------------------
def lan_ip():
    """Best-effort LAN IP so attendees on the same wifi can open the tool."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'
