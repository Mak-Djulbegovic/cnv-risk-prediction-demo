"""
Regenerate the four key statistical figures in a clean, title-less style
so they sit under native PowerPoint slide titles (no doubled titles).

Outputs: fig*_clean.png  (300 DPI, tight, white background)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from lifelines import KaplanMeierFitter
from sklearn.metrics import roc_curve, roc_auc_score
import pickle
import warnings
warnings.filterwarnings('ignore')

BASE = '/Users/makdjulbegovic/Desktop/Claude_Teach'

# ---- Clean clinical style -------------------------------------------------
NAVY   = '#16365C'   # primary
TEAL   = '#2C7A7B'   # accent / "no involvement"
CRIMSON= '#C0392B'   # risk / "involvement"
AMBER  = '#D68910'
GREEN  = '#2E8B57'
GRAY   = '#5A6570'
GRID   = '#E3E7EB'
INK    = '#212529'

mpl.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica Neue', 'Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 15,
    'axes.edgecolor': GRAY,
    'axes.linewidth': 1.1,
    'axes.labelcolor': INK,
    'axes.labelweight': 'bold',
    'axes.labelsize': 17,
    'xtick.color': INK,
    'ytick.color': INK,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'axes.grid': True,
    'grid.color': GRID,
    'grid.linewidth': 1.0,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

df = pd.read_csv(f'{BASE}/choroidal_rupture_data.csv')
print(f"Loaded {len(df)} patients")


def save(fig, name):
    fig.savefig(f'{BASE}/{name}', dpi=300, bbox_inches='tight',
                facecolor='white', pad_inches=0.15)
    plt.close(fig)
    print(f"  saved {name}")


# ---- FIGURE 1: Kaplan-Meier ----------------------------------------------
df['time'] = df.apply(
    lambda r: r['time_to_cnv_months'] if pd.notna(r['time_to_cnv_months'])
    else r['follow_up_duration_months'], axis=1)
df['event'] = (df['cnv_developed'] == 'Yes').astype(int)

fig, ax = plt.subplots(figsize=(11, 6.2))
kmf = KaplanMeierFitter()
fy = df[df['foveal_involvement'] == 'Yes']
kmf.fit(fy['time'], fy['event'], label=f'Foveal involvement  (n={len(fy)})')
kmf.plot_survival_function(ax=ax, ci_show=True, color=CRIMSON, linewidth=3)
fn = df[df['foveal_involvement'] == 'No']
kmf.fit(fn['time'], fn['event'], label=f'No foveal involvement  (n={len(fn)})')
kmf.plot_survival_function(ax=ax, ci_show=True, color=TEAL, linewidth=3)

ax.set_xlabel('Months since choroidal rupture')
ax.set_ylabel('CNV-free survival')
ax.set_ylim(0, 1.02)
ax.set_xlim(0, 36)
ax.legend(loc='upper right', fontsize=14, frameon=False)
ax.text(0.015, 0.04, 'Log-rank  p < 0.001', transform=ax.transAxes,
        fontsize=13, color=GRAY, style='italic')
save(fig, 'figure1_clean.png')


# ---- FIGURE 2: Feature importance ----------------------------------------
fi = pd.read_csv(f'{BASE}/feature_importance.csv')
names = {
    'foveal_involvement_binary': 'Foveal involvement',
    'distance_from_fovea_um': 'Distance from fovea (\u00b5m)',
    'outer_retinal_disruption_score': 'Outer retinal disruption',
    'rupture_length_mm': 'Rupture length (mm)',
    'ez_integrity_percent': 'EZ integrity (%)',
    'baseline_va_logmar': 'Baseline VA (logMAR)',
    'rpe_disruption_binary': 'RPE disruption',
    'age': 'Age',
    'subretinal_fluid_binary': 'Subretinal fluid',
    'baseline_cst_um': 'Baseline CST (\u00b5m)',
    'subretinal_hemorrhage_binary': 'Subretinal hemorrhage',
    'choroidal_thickness_um': 'Choroidal thickness (\u00b5m)',
    'intraretinal_cysts_binary': 'Intraretinal cysts',
    'sex_binary': 'Male sex',
}
fi['label'] = fi['feature'].map(names)
top = fi.head(10).iloc[::-1]  # ascending so largest on top

fig, ax = plt.subplots(figsize=(11, 6.2))
ypos = range(len(top))
# single-hue navy gradient by rank
shades = plt.cm.GnBu(np.linspace(0.45, 0.95, len(top)))
ax.barh(list(ypos), top['importance'], color=shades, edgecolor='white', height=0.72)
ax.set_yticks(list(ypos))
ax.set_yticklabels(top['label'])
ax.set_xlabel('Random forest importance')
ax.grid(axis='y', visible=False)
for i, v in enumerate(top['importance']):
    ax.text(v + 0.003, i, f'{v:.3f}', va='center', fontsize=12, color=INK)
ax.set_xlim(0, top['importance'].max() * 1.18)
save(fig, 'figure2_clean.png')


# ---- FIGURE 3: ROC --------------------------------------------------------
with open(f'{BASE}/rf_model.pkl', 'rb') as f: rf = pickle.load(f)
with open(f'{BASE}/scaler.pkl', 'rb') as f: scaler = pickle.load(f)
with open(f'{BASE}/feature_list.pkl', 'rb') as f: predictors = pickle.load(f)

df['cnv_binary'] = (df['cnv_developed'] == 'Yes').astype(int)
for col, src in [('foveal_involvement_binary', 'foveal_involvement'),
                 ('subretinal_hemorrhage_binary', 'subretinal_hemorrhage'),
                 ('rpe_disruption_binary', 'rpe_disruption'),
                 ('subretinal_fluid_binary', 'subretinal_fluid'),
                 ('intraretinal_cysts_binary', 'intraretinal_cysts'),
                 ('elm_intact_binary', 'elm_intact')]:
    df[col] = (df[src] == 'Yes').astype(int)
df['sex_binary'] = (df['sex'] == 'M').astype(int)

X = df[predictors].copy()
y = df['cnv_binary'].copy()
valid = ~X.isnull().any(axis=1)
X, y = X[valid], y[valid]
proba = rf.predict_proba(scaler.transform(X))[:, 1]
fpr, tpr, thr = roc_curve(y, proba)
auc = roc_auc_score(y, proba)

fig, ax = plt.subplots(figsize=(7.4, 6.6))
ax.plot(fpr, tpr, color=NAVY, linewidth=3.2, label=f'Random forest   AUC = {auc:.3f}')
ax.plot([0, 1], [0, 1], '--', color=GRAY, linewidth=1.8, label='Chance')
oi = np.argmax(tpr - fpr)
ax.plot(fpr[oi], tpr[oi], 'o', color=CRIMSON, markersize=11,
        label=f'Optimal threshold = {thr[oi]:.2f}')
ax.set_xlabel('1 \u2212 Specificity')
ax.set_ylabel('Sensitivity')
ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
ax.legend(loc='lower right', fontsize=13, frameon=False)
ax.set_aspect('equal')
save(fig, 'figure3_clean.png')


# ---- FIGURE 4: Risk stratification ---------------------------------------
dp = df[valid].copy()
dp['risk'] = proba
dp['grp'] = pd.cut(dp['risk'], bins=[0, 0.4, 0.7, 1.0],
                   labels=['Low\n(<40%)', 'Medium\n(40\u201370%)', 'High\n(>70%)'])
summ = dp.groupby('grp')['cnv_binary'].agg(['sum', 'count'])
summ['rate'] = summ['sum'] / summ['count'] * 100

fig, ax = plt.subplots(figsize=(8.4, 6.2))
colors = [GREEN, AMBER, CRIMSON]
bars = ax.bar(range(len(summ)), summ['rate'], color=colors, width=0.62,
              edgecolor='white', linewidth=1.5)
ax.set_xticks(range(len(summ)))
ax.set_xticklabels(summ.index)
ax.set_ylabel('Observed CNV rate (%)')
ax.set_ylim(0, 100)
ax.grid(axis='x', visible=False)
for b, rate, n in zip(bars, summ['rate'], summ['count']):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 2,
            f'{rate:.0f}%\nn={n}', ha='center', va='bottom',
            fontsize=13, fontweight='bold', color=INK)
save(fig, 'figure4_clean.png')

print("Done.")
