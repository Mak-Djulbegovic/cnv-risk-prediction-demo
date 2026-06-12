"""
Exploratory data analysis figure for the deck.

A clean 4-panel "first look at the data" that surfaces the trends BEFORE any
modeling: a categorical driver, two dose-response continuous drivers, and the
timing of CNV. Title-less so it sits under the native slide title.

Output: figure_eda_clean.png (300 DPI, white background)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings
warnings.filterwarnings('ignore')

BASE = '/Users/makdjulbegovic/Desktop/Claude_Teach'

NAVY = '#16365C'
TEAL = '#2C7A7B'
CRIMSON = '#C0392B'
AMBER = '#D68910'
GREEN = '#2E8B57'
GRAY = '#5A6570'
GRID = '#E3E7EB'
INK = '#212529'

mpl.rcParams.update({
    'figure.dpi': 300, 'savefig.dpi': 300,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica Neue', 'Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 13,
    'axes.edgecolor': GRAY, 'axes.linewidth': 1.0,
    'axes.labelcolor': INK, 'axes.labelweight': 'bold', 'axes.labelsize': 13,
    'axes.titlesize': 14, 'axes.titleweight': 'bold', 'axes.titlecolor': NAVY,
    'xtick.color': INK, 'ytick.color': INK,
    'xtick.labelsize': 11.5, 'ytick.labelsize': 11.5,
    'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.9,
    'axes.spines.top': False, 'axes.spines.right': False,
})

df = pd.read_csv(f'{BASE}/choroidal_rupture_data.csv')
df['cnv'] = (df['cnv_developed'] == 'Yes').astype(int)
print(f'Loaded {len(df)} patients')

fig, axes = plt.subplots(2, 2, figsize=(12.6, 7.0))
fig.subplots_adjust(hspace=0.42, wspace=0.26)


# ---- A: CNV rate by foveal involvement (categorical driver) ---------------
ax = axes[0, 0]
rates = df.groupby('foveal_involvement')['cnv'].mean().reindex(['No', 'Yes']) * 100
ns = df.groupby('foveal_involvement')['cnv'].size().reindex(['No', 'Yes'])
bars = ax.bar(['Fovea spared', 'Foveal involvement'], rates.values,
              color=[TEAL, CRIMSON], width=0.6, edgecolor='white', linewidth=1.5)
for b, r, n in zip(bars, rates.values, ns.values):
    ax.text(b.get_x() + b.get_width() / 2, r + 2, f'{r:.0f}%',
            ha='center', va='bottom', fontsize=13, fontweight='bold', color=INK)
ax.set_title('CNV rate by foveal involvement')
ax.set_ylabel('Developed CNV (%)')
ax.set_ylim(0, 100)
ax.grid(axis='x', visible=False)


# ---- B: CNV rate across rupture-length bins (dose-response) ----------------
ax = axes[0, 1]
df['rl_bin'] = pd.cut(df['rupture_length_mm'], bins=[0, 2, 4, 6, 12],
                      labels=['<2', '2\u20134', '4\u20136', '>6'])
rl = df.groupby('rl_bin')['cnv'].mean() * 100
ax.plot(range(len(rl)), rl.values, '-o', color=NAVY, linewidth=2.6,
        markersize=9, markerfacecolor=NAVY, markeredgecolor='white')
for i, v in enumerate(rl.values):
    ax.text(i, v + 3, f'{v:.0f}%', ha='center', va='bottom',
            fontsize=11.5, color=NAVY, fontweight='bold')
ax.set_xticks(range(len(rl)))
ax.set_xticklabels(rl.index)
ax.set_title('CNV rate rises with rupture length')
ax.set_xlabel('Rupture length (mm)')
ax.set_ylabel('Developed CNV (%)')
ax.set_ylim(0, 100)


# ---- C: CNV rate across distance-from-fovea bins (inverse trend) -----------
ax = axes[1, 0]
df['d_bin'] = pd.cut(df['distance_from_fovea_um'],
                     bins=[-1, 500, 1500, 3000, 5001],
                     labels=['<500', '500\u20131500', '1500\u20133000', '>3000'])
dd = df.groupby('d_bin')['cnv'].mean() * 100
ax.plot(range(len(dd)), dd.values, '-o', color=AMBER, linewidth=2.6,
        markersize=9, markerfacecolor=AMBER, markeredgecolor='white')
for i, v in enumerate(dd.values):
    ax.text(i, v + 3, f'{v:.0f}%', ha='center', va='bottom',
            fontsize=11.5, color='#9C6A0B', fontweight='bold')
ax.set_xticks(range(len(dd)))
ax.set_xticklabels(dd.index)
ax.set_title('CNV rate falls with distance from fovea')
ax.set_xlabel('Distance from fovea (\u00b5m)')
ax.set_ylabel('Developed CNV (%)')
ax.set_ylim(0, 100)


# ---- D: timing of CNV among those who developed it -------------------------
ax = axes[1, 1]
t = df.loc[df['cnv'] == 1, 'time_to_cnv_months'].dropna()
ax.hist(t, bins=18, color=GREEN, edgecolor='white', linewidth=0.8, alpha=0.9)
med = t.median()
ax.axvline(med, color=CRIMSON, linewidth=2, linestyle='--')
ax.text(med + 0.4, ax.get_ylim()[1] * 0.9, f'median {med:.1f} mo',
        color=CRIMSON, fontsize=11.5, fontweight='bold')
ax.set_title('When CNV appears')
ax.set_xlabel('Months to CNV')
ax.set_ylabel('Patients')
ax.grid(axis='x', visible=False)


fig.savefig(f'{BASE}/figure_eda_clean.png', dpi=300, bbox_inches='tight',
            facecolor='white', pad_inches=0.2)
plt.close(fig)
print('saved figure_eda_clean.png')
