"""
Export the trained CNV models to a single self-contained model.json so a static
browser app (GitHub Pages) reproduces the SAME numbers as the Python/Streamlit app.

- RandomForest: every tree exported with thresholds converted back to RAW feature
  space (threshold_raw = threshold_scaled * scale + mean), so the browser never
  needs the StandardScaler. Each split X_raw[f] <= t_raw is identical to the
  scaled split the model learned.
- Cox: coefficients, covariate means, and baseline cumulative hazard at months
  0..36, so S(t|x) = exp(-H0(t) * exp(sum coef*(x-mean))).
- Cohort RF risk distribution (for percentile + context histogram), median
  reference patient (for per-feature drivers), and the clinical presets.

Output: docs/model.json  (docs/ is the GitHub Pages publish folder)
"""
import json, os
import numpy as np
import cnv_core as core

rf, scaler, features, cox, cohort = core.load_artifacts()
mean = scaler.mean_; scale = scaler.scale_

# ---- RandomForest -> raw-threshold trees ----
trees = []
for est in rf.estimators_:
    t = est.tree_
    feat = t.feature.tolist()
    thr_raw = []
    for i in range(t.node_count):
        f = t.feature[i]
        if f < 0:
            thr_raw.append(0.0)
        else:
            thr_raw.append(float(t.threshold[i] * scale[f] + mean[f]))
    # leaf value = P(class 1)
    val = t.value.reshape(t.node_count, -1)
    p1 = (val[:, 1] / val.sum(axis=1)).tolist()
    trees.append({
        'l': t.children_left.tolist(),
        'r': t.children_right.tolist(),
        'f': feat,
        't': [round(x, 5) for x in thr_raw],
        'p': [round(x, 5) for x in p1],
    })

# ---- Cox ----
coef = {k: float(v) for k, v in cox.params_.items()}
cmean = {k: float(v) for k, v in cox._norm_mean.items()}
times = list(range(0, 37))
import pandas as pd
ref_patient = cox._norm_mean.to_dict()
sf = cox.predict_survival_function(pd.DataFrame([ref_patient])[core.FEATURES], times=times)
H0 = (-np.log(sf.iloc[:, 0].values.clip(1e-12, 1))).tolist()
H0[0] = 0.0  # force S(0)=1 for a clean curve

# ---- cohort risk distribution + reference row ----
dist = core.cohort_risk_distribution(rf, scaler, features, cohort).tolist()
reference = core.cohort_reference(cohort)

# ---- population Kaplan-Meier baselines (foveal yes/no) for the survival panel ----
km = {}
for fov in (True, False):
    kt, ks, kn = core.cohort_km(cohort, foveal=fov, times=times)
    km[str(fov).lower()] = {'s': [round(float(x), 5) for x in ks], 'n': int(kn)}

model = {
    'features': list(features),
    'labels': core.LABELS,
    'trees': trees,
    'cox': {'coef': coef, 'mean': cmean, 'times': times, 'H0': [round(x, 6) for x in H0]},
    'dist': [round(x, 5) for x in dist],
    'reference': reference,
    'presets': core.PRESETS,
    'km': km,
}

os.makedirs(os.path.join(core.BASE, 'docs'), exist_ok=True)
out = os.path.join(core.BASE, 'docs', 'model.json')
with open(out, 'w') as f:
    json.dump(model, f, separators=(',', ':'))
print('wrote', out, round(os.path.getsize(out) / 1024, 1), 'KB')

# ---- sanity: JS-equivalent prediction in Python matches rf.predict_proba ----
def js_predict(row):
    xs = [row[f] for f in features]
    tot = 0.0
    for tr in trees:
        n = 0
        while tr['l'][n] != -1:
            f = tr['f'][n]
            n = tr['l'][n] if xs[f] <= tr['t'][n] else tr['r'][n]
        tot += tr['p'][n]
    return tot / len(trees)

import pandas as pd
for name, raw in core.PRESETS.items():
    row = core.inputs_to_row(raw)
    py = core.predict_risk(rf, scaler, features, row)
    js = js_predict(row)
    print(f'{name:38s} python={py:.4f}  json={js:.4f}  diff={abs(py-js):.1e}')
