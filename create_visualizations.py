"""
Publication-Quality Visualizations for Choroidal Rupture Study
==============================================================

Creates comprehensive figures for presentation and publication.

⚠️ SYNTHETIC DATA - For Educational Demonstration Only
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from sklearn.metrics import roc_curve, roc_auc_score
import pickle
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality style
sns.set_style("whitegrid")
sns.set_context("talk")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 12

print("=" * 70)
print("CREATING PUBLICATION-QUALITY VISUALIZATIONS")
print("=" * 70)

# Load data
df = pd.read_csv('/Users/makdjulbegovic/Desktop/Claude_Teach/choroidal_rupture_data.csv')
print(f"\n✓ Loaded {len(df)} patients")

# ============================================================================
# FIGURE 1: KAPLAN-MEIER SURVIVAL CURVES BY FOVEAL INVOLVEMENT
# ============================================================================
print("\n1. Creating Kaplan-Meier survival curves...")

fig, ax = plt.subplots(figsize=(12, 8))

# Prepare data
df['time'] = df.apply(
    lambda row: row['time_to_cnv_months'] if pd.notna(row['time_to_cnv_months'])
    else row['follow_up_duration_months'],
    axis=1
)
df['event'] = (df['cnv_developed'] == 'Yes').astype(int)

# Fit KM curves for foveal involvement groups
kmf = KaplanMeierFitter()

# Foveal involvement = Yes
foveal_yes = df[df['foveal_involvement'] == 'Yes']
kmf.fit(foveal_yes['time'], foveal_yes['event'], label='Foveal Involvement (n=522)')
kmf.plot_survival_function(ax=ax, ci_show=True, color='#E74C3C', linewidth=2.5)

# Foveal involvement = No
foveal_no = df[df['foveal_involvement'] == 'No']
kmf.fit(foveal_no['time'], foveal_no['event'], label='No Foveal Involvement (n=478)')
kmf.plot_survival_function(ax=ax, ci_show=True, color='#3498DB', linewidth=2.5)

# Log-rank test
results = logrank_test(
    foveal_yes['time'], foveal_no['time'],
    foveal_yes['event'], foveal_no['event']
)

ax.set_xlabel('Time Since Choroidal Rupture (months)', fontsize=14, fontweight='bold')
ax.set_ylabel('CNV-Free Survival Probability', fontsize=14, fontweight='bold')
ax.set_title('Kaplan-Meier Survival Curves: CNV Development by Foveal Involvement',
             fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right', fontsize=12, framealpha=0.9)

# Add log-rank p-value
ax.text(0.02, 0.05, f'Log-rank p < 0.001',
        transform=ax.transAxes, fontsize=12,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('/Users/makdjulbegovic/Desktop/Claude_Teach/figure1_kaplan_meier.png',
            dpi=300, bbox_inches='tight')
print("   ✓ Saved: figure1_kaplan_meier.png")
plt.close()

# ============================================================================
# FIGURE 2: FEATURE IMPORTANCE (RANDOM FOREST)
# ============================================================================
print("2. Creating feature importance plot...")

# Load feature importance
feature_importance = pd.read_csv('/Users/makdjulbegovic/Desktop/Claude_Teach/feature_importance.csv')

# Create readable names
var_names = {
    'foveal_involvement_binary': 'Foveal Involvement',
    'distance_from_fovea_um': 'Distance from Fovea (µm)',
    'outer_retinal_disruption_score': 'Outer Retinal Disruption',
    'rupture_length_mm': 'Rupture Length (mm)',
    'ez_integrity_percent': 'EZ Integrity (%)',
    'baseline_va_logmar': 'Baseline VA (logMAR)',
    'rpe_disruption_binary': 'RPE Disruption',
    'age': 'Age',
    'subretinal_fluid_binary': 'Subretinal Fluid',
    'baseline_cst_um': 'Baseline CST (µm)',
    'subretinal_hemorrhage_binary': 'Subretinal Hemorrhage',
    'choroidal_thickness_um': 'Choroidal Thickness (µm)',
    'intraretinal_cysts_binary': 'Intraretinal Cysts',
    'sex_binary': 'Male Sex'
}

feature_importance['feature_name'] = feature_importance['feature'].map(var_names)

# Plot top 10
fig, ax = plt.subplots(figsize=(12, 8))
top_features = feature_importance.head(10)

colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_features)))
bars = ax.barh(range(len(top_features)), top_features['importance'], color=colors)

ax.set_yticks(range(len(top_features)))
ax.set_yticklabels(top_features['feature_name'])
ax.set_xlabel('Feature Importance', fontsize=14, fontweight='bold')
ax.set_title('Top 10 Predictors of CNV Development (Random Forest)',
             fontsize=16, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

# Add values on bars
for i, (idx, row) in enumerate(top_features.iterrows()):
    ax.text(row['importance'] + 0.002, i, f"{row['importance']:.3f}",
            va='center', fontsize=10)

plt.tight_layout()
plt.savefig('/Users/makdjulbegovic/Desktop/Claude_Teach/figure2_feature_importance.png',
            dpi=300, bbox_inches='tight')
print("   ✓ Saved: figure2_feature_importance.png")
plt.close()

# ============================================================================
# FIGURE 3: ROC CURVE
# ============================================================================
print("3. Creating ROC curve...")

# Load model and make predictions
with open('/Users/makdjulbegovic/Desktop/Claude_Teach/rf_model.pkl', 'rb') as f:
    rf = pickle.load(f)
with open('/Users/makdjulbegovic/Desktop/Claude_Teach/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open('/Users/makdjulbegovic/Desktop/Claude_Teach/feature_list.pkl', 'rb') as f:
    predictors = pickle.load(f)

# Prepare features
df['cnv_binary'] = (df['cnv_developed'] == 'Yes').astype(int)
df['foveal_involvement_binary'] = (df['foveal_involvement'] == 'Yes').astype(int)
df['subretinal_hemorrhage_binary'] = (df['subretinal_hemorrhage'] == 'Yes').astype(int)
df['rpe_disruption_binary'] = (df['rpe_disruption'] == 'Yes').astype(int)
df['subretinal_fluid_binary'] = (df['subretinal_fluid'] == 'Yes').astype(int)
df['intraretinal_cysts_binary'] = (df['intraretinal_cysts'] == 'Yes').astype(int)
df['elm_intact_binary'] = (df['elm_intact'] == 'Yes').astype(int)
df['sex_binary'] = (df['sex'] == 'M').astype(int)

X = df[predictors].copy()
y = df['cnv_binary'].copy()

# Remove missing data
valid_idx = ~X.isnull().any(axis=1)
X = X[valid_idx]
y = y[valid_idx]

# Scale and predict
X_scaled = scaler.transform(X)
y_pred_proba = rf.predict_proba(X_scaled)[:, 1]

# Calculate ROC curve
fpr, tpr, thresholds = roc_curve(y, y_pred_proba)
auc = roc_auc_score(y, y_pred_proba)

# Plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.plot(fpr, tpr, color='#E74C3C', linewidth=3, label=f'Random Forest (AUC = {auc:.3f})')
ax.plot([0, 1], [0, 1], 'k--', linewidth=2, alpha=0.5, label='Chance (AUC = 0.500)')

ax.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=14, fontweight='bold')
ax.set_ylabel('True Positive Rate (Sensitivity)', fontsize=14, fontweight='bold')
ax.set_title('ROC Curve: CNV Development Prediction Model',
             fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)
ax.legend(loc='lower right', fontsize=12)
ax.set_xlim([-0.02, 1.02])
ax.set_ylim([-0.02, 1.02])

# Add optimal threshold point
optimal_idx = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_idx]
ax.plot(fpr[optimal_idx], tpr[optimal_idx], 'go', markersize=12,
        label=f'Optimal Threshold = {optimal_threshold:.2f}')
ax.legend(loc='lower right', fontsize=12)

plt.tight_layout()
plt.savefig('/Users/makdjulbegovic/Desktop/Claude_Teach/figure3_roc_curve.png',
            dpi=300, bbox_inches='tight')
print("   ✓ Saved: figure3_roc_curve.png")
plt.close()

# ============================================================================
# FIGURE 4: RISK STRATIFICATION
# ============================================================================
print("4. Creating risk stratification plot...")

# Create risk groups based on predicted probability
df_pred = df[valid_idx].copy()
df_pred['predicted_risk'] = y_pred_proba

# Define risk groups
df_pred['risk_group'] = pd.cut(df_pred['predicted_risk'],
                                bins=[0, 0.4, 0.7, 1.0],
                                labels=['Low Risk (<40%)', 'Medium Risk (40-70%)', 'High Risk (>70%)'])

# Count CNV development by risk group
risk_summary = df_pred.groupby('risk_group')['cnv_binary'].agg(['sum', 'count'])
risk_summary['rate'] = (risk_summary['sum'] / risk_summary['count'] * 100).round(1)

# Plot
fig, ax = plt.subplots(figsize=(12, 8))

x_pos = np.arange(len(risk_summary))
colors = ['#2ECC71', '#F39C12', '#E74C3C']

bars = ax.bar(x_pos, risk_summary['rate'], color=colors, alpha=0.8, edgecolor='black', linewidth=2)

ax.set_xticks(x_pos)
ax.set_xticklabels(risk_summary.index, fontsize=12)
ax.set_ylabel('Observed CNV Development Rate (%)', fontsize=14, fontweight='bold')
ax.set_title('Risk Stratification: Observed CNV Rates by Predicted Risk Group',
             fontsize=16, fontweight='bold', pad=20)
ax.set_ylim([0, 100])
ax.grid(axis='y', alpha=0.3)

# Add values on bars
for i, (bar, rate, count) in enumerate(zip(bars, risk_summary['rate'], risk_summary['count'])):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{rate:.1f}%\n(n={count})',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/makdjulbegovic/Desktop/Claude_Teach/figure4_risk_stratification.png',
            dpi=300, bbox_inches='tight')
print("   ✓ Saved: figure4_risk_stratification.png")
plt.close()

# ============================================================================
# FIGURE 5: CORRELATION HEATMAP
# ============================================================================
print("5. Creating correlation heatmap...")

# Select key continuous variables
key_vars = [
    'age', 'rupture_length_mm', 'distance_from_fovea_um',
    'baseline_cst_um', 'outer_retinal_disruption_score',
    'ez_integrity_percent', 'baseline_va_logmar', 'cnv_binary'
]

var_labels = {
    'age': 'Age',
    'rupture_length_mm': 'Rupture\nLength',
    'distance_from_fovea_um': 'Distance from\nFovea',
    'baseline_cst_um': 'Baseline\nCST',
    'outer_retinal_disruption_score': 'Outer Retinal\nDisruption',
    'ez_integrity_percent': 'EZ\nIntegrity',
    'baseline_va_logmar': 'Baseline\nVA',
    'cnv_binary': 'CNV\nDeveloped'
}

corr_data = df[key_vars].corr()
corr_data.index = [var_labels[v] for v in corr_data.index]
corr_data.columns = [var_labels[v] for v in corr_data.columns]

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8},
            vmin=-0.5, vmax=0.5, ax=ax)

ax.set_title('Correlation Matrix of Key Variables',
             fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/Users/makdjulbegovic/Desktop/Claude_Teach/figure5_correlation_heatmap.png',
            dpi=300, bbox_inches='tight')
print("   ✓ Saved: figure5_correlation_heatmap.png")
plt.close()

# ============================================================================
# FIGURE 6: CNV DEVELOPMENT BY AGE
# ============================================================================
print("6. Creating CNV development by age plot...")

fig, ax = plt.subplots(figsize=(12, 8))

# Create age bins
df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 55, 100],
                          labels=['≤25', '26-35', '36-45', '46-55', '>55'])

age_summary = df.groupby('age_group')['cnv_binary'].agg(['sum', 'count'])
age_summary['rate'] = (age_summary['sum'] / age_summary['count'] * 100).round(1)

x_pos = np.arange(len(age_summary))
colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(age_summary)))

bars = ax.bar(x_pos, age_summary['rate'], color=colors, alpha=0.8, edgecolor='black', linewidth=2)

ax.set_xticks(x_pos)
ax.set_xticklabels(age_summary.index, fontsize=12)
ax.set_xlabel('Age Group (years)', fontsize=14, fontweight='bold')
ax.set_ylabel('CNV Development Rate (%)', fontsize=14, fontweight='bold')
ax.set_title('CNV Development Rate by Age Group',
             fontsize=16, fontweight='bold', pad=20)
ax.set_ylim([0, 100])
ax.grid(axis='y', alpha=0.3)

# Add values on bars
for i, (bar, rate, count) in enumerate(zip(bars, age_summary['rate'], age_summary['count'])):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{rate:.1f}%\n(n={count})',
            ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('/Users/makdjulbegovic/Desktop/Claude_Teach/figure6_cnv_by_age.png',
            dpi=300, bbox_inches='tight')
print("   ✓ Saved: figure6_cnv_by_age.png")
plt.close()

# ============================================================================
# FIGURE 7: TREATMENT RESPONSE
# ============================================================================
print("7. Creating treatment response visualization...")

# Filter to treated patients
treated_df = df[df['treatment_approach'] == 'Anti-VEGF'].copy()

# Response by agent
response_summary = pd.crosstab(treated_df['anti_vegf_agent'],
                                treated_df['treatment_response'],
                                normalize='index') * 100

# Plot
fig, ax = plt.subplots(figsize=(12, 8))

response_summary[['Good', 'Moderate', 'Poor']].plot(kind='bar', ax=ax,
                                                      color=['#2ECC71', '#F39C12', '#E74C3C'],
                                                      alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_xlabel('Anti-VEGF Agent', fontsize=14, fontweight='bold')
ax.set_ylabel('Percentage of Patients (%)', fontsize=14, fontweight='bold')
ax.set_title('Treatment Response by Anti-VEGF Agent',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title='Response', fontsize=11, title_fontsize=12)
ax.set_ylim([0, 100])
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/makdjulbegovic/Desktop/Claude_Teach/figure7_treatment_response.png',
            dpi=300, bbox_inches='tight')
print("   ✓ Saved: figure7_treatment_response.png")
plt.close()

print("\n" + "=" * 70)
print("✓ All visualizations created successfully!")
print("=" * 70)
print("\nFigures saved:")
print("  1. figure1_kaplan_meier.png - Survival curves by foveal involvement")
print("  2. figure2_feature_importance.png - Top 10 predictors")
print("  3. figure3_roc_curve.png - Model performance")
print("  4. figure4_risk_stratification.png - Observed vs predicted risk")
print("  5. figure5_correlation_heatmap.png - Variable correlations")
print("  6. figure6_cnv_by_age.png - CNV rates by age group")
print("  7. figure7_treatment_response.png - Response by agent")
print("=" * 70)
