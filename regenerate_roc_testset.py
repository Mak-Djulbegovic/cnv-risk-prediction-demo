"""
Regenerate figure3_clean.png (ROC) HONESTLY.

The previous version scored the random forest on the full dataset (the same
rows it trained on), which inflates AUC. This evaluates the pickled model on
the held-out 20% test split (test_size=0.2, random_state=42, stratify=y) -
the same split that produced the reported test AUC - so the figure matches the
rest of the deck and teaches out-of-sample evaluation honestly.

Output: figure3_clean.png (300 DPI, white background), style-matched.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

import cnv_core as core

NAVY = '#16365C'
GRAY = '#5A6570'
CRIMSON = '#C0392B'
GRID = '#E3E7EB'
INK = '#212529'

mpl.rcParams.update({
    'figure.dpi': 300, 'savefig.dpi': 300,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica Neue', 'Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 15,
    'axes.edgecolor': GRAY, 'axes.linewidth': 1.1,
    'axes.labelcolor': INK, 'axes.labelweight': 'bold', 'axes.labelsize': 17,
    'xtick.color': INK, 'ytick.color': INK,
    'xtick.labelsize': 14, 'ytick.labelsize': 14,
    'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 1.0,
    'axes.spines.top': False, 'axes.spines.right': False,
})

rf, scaler, features, cox, cohort = core.load_artifacts()
df = core._binarize_cohort(cohort)
X = df[features].copy()
y = (df['cnv_developed'] == 'Yes').astype(int)
valid = ~X.isnull().any(axis=1)
X, y = X[valid], y[valid]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

proba = rf.predict_proba(scaler.transform(X_test))[:, 1]
fpr, tpr, thr = roc_curve(y_test, proba)
auc = roc_auc_score(y_test, proba)
print(f'Held-out test set: n={len(y_test)}  AUC={auc:.3f}')

fig, ax = plt.subplots(figsize=(7.4, 6.6))
ax.plot(fpr, tpr, color=NAVY, linewidth=3.2,
        label=f'Random forest   AUC = {auc:.2f}')
ax.plot([0, 1], [0, 1], '--', color=GRAY, linewidth=1.8, label='Chance')
oi = np.argmax(tpr - fpr)
ax.plot(fpr[oi], tpr[oi], 'o', color=CRIMSON, markersize=11,
        label=f'Optimal threshold = {thr[oi]:.2f}')
ax.text(0.03, 0.97, f'Held-out test set  (n = {len(y_test)})', transform=ax.transAxes,
        ha='left', va='top', fontsize=13, color=GRAY, style='italic')
ax.set_xlabel('1 \u2212 Specificity')
ax.set_ylabel('Sensitivity')
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.legend(loc='lower right', fontsize=13, frameon=False)
ax.set_aspect('equal')
fig.savefig(f'{core.BASE}/figure3_clean.png', dpi=300, bbox_inches='tight',
            facecolor='white', pad_inches=0.15)
plt.close(fig)
print('saved figure3_clean.png')
