"""
Exploratory Data Analysis for Choroidal Rupture Study
======================================================

This script performs comprehensive exploratory analysis on the synthetic dataset.

⚠️ SYNTHETIC DATA - For Educational Demonstration Only
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

print("=" * 70)
print("EXPLORATORY DATA ANALYSIS - CHOROIDAL RUPTURE STUDY")
print("=" * 70)

# ============================================================================
# LOAD DATA
# ============================================================================
print("\n1. Loading data...")
df = pd.read_csv('/Users/makdjulbegovic/Desktop/Claude_Teach/choroidal_rupture_data.csv')
print(f"   ✓ Loaded {len(df)} patients with {len(df.columns)} variables")

# ============================================================================
# DESCRIPTIVE STATISTICS
# ============================================================================
print("\n2. DESCRIPTIVE STATISTICS")
print("=" * 70)

print("\nDEMOGRAPHICS:")
print(f"  Total patients: {len(df)}")
print(f"  Age: {df['age'].mean():.1f} ± {df['age'].std():.1f} years")
print(f"    Range: {df['age'].min()}-{df['age'].max()} years")
print(f"  Sex distribution:")
print(f"    Male: {(df['sex'] == 'M').sum()} ({(df['sex'] == 'M').sum()/len(df)*100:.1f}%)")
print(f"    Female: {(df['sex'] == 'F').sum()} ({(df['sex'] == 'F').sum()/len(df)*100:.1f}%)")

print(f"\n  Race distribution:")
for race in df['race'].unique():
    count = (df['race'] == race).sum()
    print(f"    {race}: {count} ({count/len(df)*100:.1f}%)")

print(f"\n  Occupation risk:")
for risk in ['High', 'Medium', 'Low']:
    count = (df['occupation_risk'] == risk).sum()
    print(f"    {risk}: {count} ({count/len(df)*100:.1f}%)")

print("\n" + "-" * 70)
print("INJURY CHARACTERISTICS:")
print(f"  Mechanism of injury:")
for mechanism in df['mechanism_of_injury'].value_counts().index[:5]:
    count = (df['mechanism_of_injury'] == mechanism).sum()
    print(f"    {mechanism}: {count} ({count/len(df)*100:.1f}%)")

print(f"\n  Rupture length: {df['rupture_length_mm'].mean():.2f} ± {df['rupture_length_mm'].std():.2f} mm")
print(f"    Range: {df['rupture_length_mm'].min():.2f}-{df['rupture_length_mm'].max():.2f} mm")

print(f"  Distance from fovea: {df['distance_from_fovea_um'].mean():.0f} ± {df['distance_from_fovea_um'].std():.0f} µm")
print(f"    Range: {df['distance_from_fovea_um'].min():.0f}-{df['distance_from_fovea_um'].max():.0f} µm")

print(f"  Foveal involvement: {(df['foveal_involvement'] == 'Yes').sum()} ({(df['foveal_involvement'] == 'Yes').sum()/len(df)*100:.1f}%)")
print(f"  Subretinal hemorrhage: {(df['subretinal_hemorrhage'] == 'Yes').sum()} ({(df['subretinal_hemorrhage'] == 'Yes').sum()/len(df)*100:.1f}%)")

print("\n" + "-" * 70)
print("BASELINE OCT PARAMETERS:")
print(f"  Central subfield thickness: {df['baseline_cst_um'].mean():.0f} ± {df['baseline_cst_um'].std():.0f} µm")
print(f"  Outer retinal disruption score: {df['outer_retinal_disruption_score'].mean():.2f} ± {df['outer_retinal_disruption_score'].std():.2f}")
print(f"    Score distribution: 0={((df['outer_retinal_disruption_score']==0).sum())}, " +
      f"1={((df['outer_retinal_disruption_score']==1).sum())}, " +
      f"2={((df['outer_retinal_disruption_score']==2).sum())}, " +
      f"3={((df['outer_retinal_disruption_score']==3).sum())}")
print(f"  RPE disruption: {(df['rpe_disruption'] == 'Yes').sum()} ({(df['rpe_disruption'] == 'Yes').sum()/len(df)*100:.1f}%)")
print(f"  Ellipsoid zone integrity: {df['ez_integrity_percent'].mean():.1f} ± {df['ez_integrity_percent'].std():.1f}%")
print(f"  Subretinal fluid: {(df['subretinal_fluid'] == 'Yes').sum()} ({(df['subretinal_fluid'] == 'Yes').sum()/len(df)*100:.1f}%)")
print(f"  Intraretinal cysts: {(df['intraretinal_cysts'] == 'Yes').sum()} ({(df['intraretinal_cysts'] == 'Yes').sum()/len(df)*100:.1f}%)")

print("\n" + "-" * 70)
print("VISUAL ACUITY:")
print(f"  Baseline VA (logMAR): {df['baseline_va_logmar'].mean():.2f} ± {df['baseline_va_logmar'].std():.2f}")
print(f"    Approximate Snellen: 20/{10**(df['baseline_va_logmar'].mean()) * 20:.0f}")
print(f"  Final VA (logMAR): {df['final_va_logmar'].mean():.2f} ± {df['final_va_logmar'].std():.2f}")
print(f"    Approximate Snellen: 20/{10**(df['final_va_logmar'].mean()) * 20:.0f}")
print(f"  Mean VA change: {(df['final_va_logmar'] - df['baseline_va_logmar']).mean():.2f} logMAR")

print("\n" + "-" * 70)
print("PRIMARY OUTCOME - CNV DEVELOPMENT:")
cnv_count = (df['cnv_developed'] == 'Yes').sum()
print(f"  CNV developed: {cnv_count} patients ({cnv_count/len(df)*100:.1f}%)")
print(f"  Time to CNV (in those who developed CNV):")
print(f"    Mean: {df[df['cnv_developed']=='Yes']['time_to_cnv_months'].mean():.1f} months")
print(f"    Median: {df[df['cnv_developed']=='Yes']['time_to_cnv_months'].median():.1f} months")
print(f"    Range: {df[df['cnv_developed']=='Yes']['time_to_cnv_months'].min():.1f}-{df[df['cnv_developed']=='Yes']['time_to_cnv_months'].max():.1f} months")

print(f"\n  CNV type distribution (among those with CNV):")
for cnv_type in ['Classic', 'Occult', 'Mixed']:
    count = (df['cnv_type'] == cnv_type).sum()
    print(f"    {cnv_type}: {count} ({count/cnv_count*100:.1f}% of CNV cases)")

print("\n" + "-" * 70)
print("TREATMENT:")
print(f"  Treatment approach:")
for tx in df['treatment_approach'].value_counts().index:
    count = (df['treatment_approach'] == tx).sum()
    print(f"    {tx}: {count} ({count/len(df)*100:.1f}%)")

treated_df = df[df['treatment_approach'] == 'Anti-VEGF']
print(f"\n  Anti-VEGF agent distribution (n={len(treated_df)}):")
for agent in ['Eylea', 'Lucentis', 'Avastin']:
    count = (treated_df['anti_vegf_agent'] == agent).sum()
    print(f"    {agent}: {count} ({count/len(treated_df)*100:.1f}%)")

print(f"\n  Number of injections (in treated patients):")
print(f"    Mean: {treated_df['number_of_injections'].mean():.1f} ± {treated_df['number_of_injections'].std():.1f}")
print(f"    Range: {treated_df['number_of_injections'].min()}-{treated_df['number_of_injections'].max()}")

print(f"\n  Treatment response (in treated patients):")
for response in ['Good', 'Moderate', 'Poor']:
    count = (treated_df['treatment_response'] == response).sum()
    print(f"    {response}: {count} ({count/len(treated_df)*100:.1f}%)")

# ============================================================================
# UNIVARIATE ANALYSIS - CNV RISK FACTORS
# ============================================================================
print("\n\n3. UNIVARIATE ANALYSIS - CNV RISK FACTORS")
print("=" * 70)

# Continuous variables
print("\nCONTINUOUS VARIABLES:")
print(f"{'Variable':<35} {'CNV Yes':<20} {'CNV No':<20} {'p-value':<10}")
print("-" * 85)

continuous_vars = [
    ('age', 'Age (years)'),
    ('rupture_length_mm', 'Rupture length (mm)'),
    ('distance_from_fovea_um', 'Distance from fovea (µm)'),
    ('baseline_cst_um', 'Baseline CST (µm)'),
    ('outer_retinal_disruption_score', 'Outer retinal disruption'),
    ('ez_integrity_percent', 'EZ integrity (%)'),
    ('baseline_va_logmar', 'Baseline VA (logMAR)')
]

for var, label in continuous_vars:
    cnv_yes = df[df['cnv_developed'] == 'Yes'][var]
    cnv_no = df[df['cnv_developed'] == 'No'][var]

    # t-test
    t_stat, p_value = stats.ttest_ind(cnv_yes, cnv_no)

    print(f"{label:<35} {cnv_yes.mean():.1f} ± {cnv_yes.std():.1f}    " +
          f"{cnv_no.mean():.1f} ± {cnv_no.std():.1f}    " +
          f"{'<0.001' if p_value < 0.001 else f'{p_value:.3f}'}")

print("\n\nCATEGORICAL VARIABLES:")
print(f"{'Variable':<35} {'CNV Rate':<20} {'p-value':<10}")
print("-" * 65)

categorical_vars = [
    ('sex', 'Sex (Male)'),
    ('foveal_involvement', 'Foveal involvement'),
    ('subretinal_hemorrhage', 'Subretinal hemorrhage'),
    ('rpe_disruption', 'RPE disruption'),
    ('subretinal_fluid', 'Subretinal fluid'),
    ('intraretinal_cysts', 'Intraretinal cysts')
]

for var, label in categorical_vars:
    if var == 'sex':
        group = df[df[var] == 'M']
        group_label = 'Male'
    else:
        group = df[df[var] == 'Yes']
        group_label = 'Yes'

    cnv_rate = (group['cnv_developed'] == 'Yes').sum() / len(group) * 100

    # Chi-square test
    contingency = pd.crosstab(df[var], df['cnv_developed'])
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

    print(f"{label:<35} {cnv_rate:.1f}%                " +
          f"{'<0.001' if p_value < 0.001 else f'{p_value:.3f}'}")

# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================
print("\n\n4. CORRELATION ANALYSIS")
print("=" * 70)

# Select numeric columns for correlation
numeric_cols = [
    'age', 'rupture_length_mm', 'distance_from_fovea_um',
    'baseline_cst_um', 'outer_retinal_disruption_score',
    'ez_integrity_percent', 'baseline_va_logmar', 'time_to_cnv_months'
]

# Create binary CNV variable
df['cnv_binary'] = (df['cnv_developed'] == 'Yes').astype(int)

print("\nCorrelation with CNV Development:")
print("-" * 50)
for col in numeric_cols[:-1]:  # Exclude time_to_cnv_months
    corr = df[col].corr(df['cnv_binary'])
    print(f"  {col:<40} r = {corr:>6.3f}")

# ============================================================================
# CREATE SUMMARY TABLES
# ============================================================================
print("\n\n5. CREATING SUMMARY TABLES")
print("=" * 70)

# Table 1: Patient Characteristics by CNV Status
print("\nTable 1: Patient Characteristics by CNV Status")
print("-" * 70)

summary_stats = []

# Demographics
summary_stats.append({
    'Characteristic': 'Age (years), mean ± SD',
    'CNV Yes (n=634)': f"{df[df['cnv_developed']=='Yes']['age'].mean():.1f} ± {df[df['cnv_developed']=='Yes']['age'].std():.1f}",
    'CNV No (n=366)': f"{df[df['cnv_developed']=='No']['age'].mean():.1f} ± {df[df['cnv_developed']=='No']['age'].std():.1f}"
})

summary_stats.append({
    'Characteristic': 'Male sex, n (%)',
    'CNV Yes (n=634)': f"{(df[df['cnv_developed']=='Yes']['sex']=='M').sum()} ({(df[df['cnv_developed']=='Yes']['sex']=='M').sum()/634*100:.1f}%)",
    'CNV No (n=366)': f"{(df[df['cnv_developed']=='No']['sex']=='M').sum()} ({(df[df['cnv_developed']=='No']['sex']=='M').sum()/366*100:.1f}%)"
})

summary_stats.append({
    'Characteristic': 'Foveal involvement, n (%)',
    'CNV Yes (n=634)': f"{(df[df['cnv_developed']=='Yes']['foveal_involvement']=='Yes').sum()} ({(df[df['cnv_developed']=='Yes']['foveal_involvement']=='Yes').sum()/634*100:.1f}%)",
    'CNV No (n=366)': f"{(df[df['cnv_developed']=='No']['foveal_involvement']=='Yes').sum()} ({(df[df['cnv_developed']=='No']['foveal_involvement']=='Yes').sum()/366*100:.1f}%)"
})

summary_stats.append({
    'Characteristic': 'Rupture length (mm), mean ± SD',
    'CNV Yes (n=634)': f"{df[df['cnv_developed']=='Yes']['rupture_length_mm'].mean():.2f} ± {df[df['cnv_developed']=='Yes']['rupture_length_mm'].std():.2f}",
    'CNV No (n=366)': f"{df[df['cnv_developed']=='No']['rupture_length_mm'].mean():.2f} ± {df[df['cnv_developed']=='No']['rupture_length_mm'].std():.2f}"
})

summary_table = pd.DataFrame(summary_stats)
print(summary_table.to_string(index=False))

# Save summary table
summary_table.to_csv('/Users/makdjulbegovic/Desktop/Claude_Teach/summary_table1.csv', index=False)
print("\n✓ Summary table saved to: summary_table1.csv")

# ============================================================================
# MISSING DATA CHECK
# ============================================================================
print("\n\n6. MISSING DATA CHECK")
print("=" * 70)
missing_counts = df.isnull().sum()
missing_pct = (missing_counts / len(df) * 100).round(1)

print("\nVariables with missing data:")
for col in df.columns:
    if missing_counts[col] > 0:
        print(f"  {col:<40} {missing_counts[col]:>5} ({missing_pct[col]:>5.1f}%)")

if missing_counts.sum() == 0:
    print("  No missing data detected (except expected NaN for non-CNV cases)")
else:
    print(f"\nNote: time_to_cnv_months is expected to be missing for patients without CNV")

print("\n" + "=" * 70)
print("✓ Exploratory analysis complete!")
print("=" * 70)
