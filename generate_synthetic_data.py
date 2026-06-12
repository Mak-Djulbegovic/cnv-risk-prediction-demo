"""
Synthetic Database Generator for Choroidal Rupture Study
=========================================================

This script generates a synthetic dataset of 1000 patients with traumatic choroidal rupture.
Data is based on published literature and includes realistic correlations between variables.

⚠️ SYNTHETIC DATA - For Educational Demonstration Only

Literature References:
- Ament CS, et al. Ophthalmology. 2006 (CNV incidence ~20-30% post-rupture)
- Gross NE, et al. Retina. 2001 (Risk factors for CNV development)
- Gass JD. Arch Ophthalmol. 1987 (Natural history of choroidal rupture)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Number of patients
N_PATIENTS = 1000

print(f"Generating synthetic database for {N_PATIENTS} patients...")
print("=" * 60)

# ============================================================================
# DEMOGRAPHICS
# ============================================================================
print("\n1. Generating demographics...")

data = {
    'patient_id': [f'CR{str(i).zfill(4)}' for i in range(1, N_PATIENTS + 1)],

    # Age: Younger patients more common in trauma (mean ~35, SD 15)
    'age': np.clip(np.random.normal(35, 15, N_PATIENTS).astype(int), 10, 85),

    # Sex: Male predominance in ocular trauma (~75%)
    'sex': np.random.choice(['M', 'F'], N_PATIENTS, p=[0.75, 0.25]),

    # Race distribution
    'race': np.random.choice(
        ['White', 'Black', 'Hispanic', 'Asian', 'Other'],
        N_PATIENTS,
        p=[0.45, 0.25, 0.18, 0.08, 0.04]
    ),

    # Occupation risk (manual labor higher risk for trauma)
    'occupation_risk': np.random.choice(
        ['High', 'Medium', 'Low'],
        N_PATIENTS,
        p=[0.35, 0.40, 0.25]
    )
}

# ============================================================================
# INJURY CHARACTERISTICS
# ============================================================================
print("2. Generating injury characteristics...")

# Mechanism of injury
data['mechanism_of_injury'] = np.random.choice(
    ['Blunt trauma', 'Motor vehicle accident', 'Sports injury', 'Fall', 'Assault', 'Other'],
    N_PATIENTS,
    p=[0.30, 0.25, 0.20, 0.12, 0.08, 0.05]
)

# Rupture location (clock hours) - inferior more common (6 o'clock region)
data['rupture_location_clock_hours'] = np.random.choice(
    range(1, 13),
    N_PATIENTS,
    p=[0.06, 0.06, 0.06, 0.08, 0.10, 0.15, 0.15, 0.10, 0.08, 0.06, 0.06, 0.04]
)

# Rupture length in mm (mean 3.5mm, range 0.5-12mm)
data['rupture_length_mm'] = np.clip(np.random.gamma(2, 1.5, N_PATIENTS), 0.5, 12.0).round(2)

# Distance from fovea (micrometers) - influences prognosis
# Closer to fovea = worse prognosis
data['distance_from_fovea_um'] = np.clip(
    np.random.exponential(800, N_PATIENTS).astype(int),
    0, 5000
)

# Foveal involvement (if distance < 500um, likely involved)
data['foveal_involvement'] = ['Yes' if d < 500 else 'No'
                               for d in data['distance_from_fovea_um']]
# Add some randomness
foveal_mask = np.random.random(N_PATIENTS) < 0.1
data['foveal_involvement'] = [
    'Yes' if (data['foveal_involvement'][i] == 'Yes' or foveal_mask[i]) else 'No'
    for i in range(N_PATIENTS)
]

# Choroidal thickness at rupture site (150-450 um, thinner = worse)
data['choroidal_thickness_um'] = np.clip(
    np.random.normal(280, 60, N_PATIENTS).astype(int),
    150, 450
)

# Time to presentation (0-30 days, most present within first week)
data['time_to_presentation_days'] = np.clip(
    np.random.exponential(3, N_PATIENTS).astype(int),
    0, 30
)

# Subretinal hemorrhage (70% have some hemorrhage)
data['subretinal_hemorrhage'] = np.random.choice(['Yes', 'No'], N_PATIENTS, p=[0.70, 0.30])

# ============================================================================
# BASELINE OCT PARAMETERS
# ============================================================================
print("3. Generating baseline OCT parameters...")

# Central subfield thickness (normal ~250um, can be elevated with edema)
baseline_cst_mean = np.where(
    data['foveal_involvement'] == 'Yes',
    350,  # Higher if fovea involved
    280   # Lower if peripheral
)
data['baseline_cst_um'] = np.clip(
    np.random.normal(baseline_cst_mean, 50, N_PATIENTS).astype(int),
    180, 600
)

# Outer retinal disruption score (0=none, 1=mild, 2=moderate, 3=severe)
# Worse if fovea involved
disruption_scores = []
for i in range(N_PATIENTS):
    if data['foveal_involvement'][i] == 'Yes':
        # More severe if fovea involved
        score = np.random.choice([0, 1, 2, 3], p=[0.05, 0.15, 0.35, 0.45])
    else:
        # Less severe if peripheral
        score = np.random.choice([0, 1, 2, 3], p=[0.25, 0.35, 0.25, 0.15])
    disruption_scores.append(score)
data['outer_retinal_disruption_score'] = disruption_scores

# RPE disruption (correlated with outer retinal disruption)
rpe_prob = 0.3 + 0.2 * np.array(data['outer_retinal_disruption_score']) / 3
data['rpe_disruption'] = [
    'Yes' if np.random.random() < rpe_prob[i] else 'No'
    for i in range(N_PATIENTS)
]

# Subfoveal choroidal thickness (200-450 um)
data['subfoveal_choroidal_thickness_um'] = np.clip(
    np.random.normal(320, 70, N_PATIENTS).astype(int),
    200, 500
)

# Subretinal fluid (40% have SRF acutely)
data['subretinal_fluid'] = np.random.choice(['Yes', 'No'], N_PATIENTS, p=[0.40, 0.60])

# Intraretinal cysts (25% have cysts)
data['intraretinal_cysts'] = np.random.choice(['Yes', 'No'], N_PATIENTS, p=[0.25, 0.75])

# Ellipsoid zone integrity (0-100%, lower = worse)
ez_mean = np.where(
    np.array(data['outer_retinal_disruption_score']) >= 2,
    40,  # Poor if severe disruption
    75   # Better if mild disruption
)
data['ez_integrity_percent'] = np.clip(
    np.random.normal(ez_mean, 20, N_PATIENTS).astype(int),
    0, 100
)

# External limiting membrane intact (related to EZ integrity)
elm_prob = data['ez_integrity_percent'] / 150  # Higher EZ → more likely intact ELM
data['elm_intact'] = [
    'Yes' if np.random.random() < p else 'No'
    for p in elm_prob
]

# OCT quality score (1-10, 10=excellent)
data['oct_quality_score'] = np.random.choice(range(5, 11), N_PATIENTS, p=[0.05, 0.10, 0.15, 0.25, 0.25, 0.20])

# ============================================================================
# TREATMENT
# ============================================================================
print("4. Generating treatment data...")

# Treatment approach: Observation mostly, unless CNV develops
# We'll assign this initially, then modify based on CNV status
data['treatment_approach'] = ['Observation'] * N_PATIENTS  # Will update later

data['anti_vegf_agent'] = ['None'] * N_PATIENTS  # Will update based on treatment
data['number_of_injections'] = [0] * N_PATIENTS  # Will update based on treatment
data['supplemental_laser'] = ['No'] * N_PATIENTS  # 5% get laser

# ============================================================================
# VISUAL ACUITY
# ============================================================================
print("5. Generating visual acuity data...")

# Baseline VA (logMAR) - worse if fovea involved
# Normal = 0.0 logMAR (20/20), 1.0 = 20/200
baseline_va_mean = np.where(
    np.array(data['foveal_involvement']) == 'Yes',
    0.8,  # ~20/125 if fovea involved
    0.3   # ~20/40 if peripheral
)
# Add effect of outer retinal disruption
baseline_va_mean = baseline_va_mean + 0.15 * np.array(data['outer_retinal_disruption_score'])

data['baseline_va_logmar'] = np.clip(
    np.random.normal(baseline_va_mean, 0.25, N_PATIENTS),
    0.0, 2.0
).round(2)

# ============================================================================
# OUTCOMES - CNV DEVELOPMENT (This is the key outcome)
# ============================================================================
print("6. Generating outcomes (CNV development)...")

# CNV development based on risk factors:
# Risk factors (from literature):
# 1. Younger age (higher risk)
# 2. Foveal involvement (higher risk)
# 3. Larger rupture size (higher risk)
# 4. Closer to fovea (higher risk)
# 5. Greater outer retinal disruption (higher risk)

# Base CNV incidence ~25%
cnv_risk = np.full(N_PATIENTS, 0.25)

# Age effect: Younger = higher risk (decrease 0.5% per year above 30)
cnv_risk -= (np.array(data['age']) - 30) * 0.005
cnv_risk = np.clip(cnv_risk, 0.05, 0.70)

# Foveal involvement: +25% risk
cnv_risk[np.array(data['foveal_involvement']) == 'Yes'] += 0.25

# Rupture length: +3% per mm
cnv_risk += np.array(data['rupture_length_mm']) * 0.03

# Outer retinal disruption: +10% per severity level
cnv_risk += np.array(data['outer_retinal_disruption_score']) * 0.10

# Distance from fovea: Closer = higher risk
cnv_risk += (1000 - np.clip(data['distance_from_fovea_um'], 0, 1000)) / 1000 * 0.15

# Clip final risk to realistic range
cnv_risk = np.clip(cnv_risk, 0.05, 0.80)

# Generate CNV development
data['cnv_developed'] = [
    'Yes' if np.random.random() < risk else 'No'
    for risk in cnv_risk
]

cnv_count = sum(1 for x in data['cnv_developed'] if x == 'Yes')
print(f"   → {cnv_count} patients ({cnv_count/N_PATIENTS*100:.1f}%) developed CNV")

# Time to CNV development (if CNV developed)
# Mean ~8 months, range 1-36 months
# Faster development in high-risk patients
time_to_cnv_mean = np.where(
    cnv_risk > 0.5,
    6,   # Faster in high-risk
    10   # Slower in lower-risk
)

data['time_to_cnv_months'] = [
    np.clip(np.random.gamma(2, time_to_cnv_mean[i]/2, 1)[0], 1, 36).round(1)
    if data['cnv_developed'][i] == 'Yes' else np.nan
    for i in range(N_PATIENTS)
]

# CNV type (if CNV developed)
data['cnv_type'] = [
    np.random.choice(['Classic', 'Occult', 'Mixed'], p=[0.30, 0.45, 0.25])
    if data['cnv_developed'][i] == 'Yes' else 'None'
    for i in range(N_PATIENTS)
]

# ============================================================================
# UPDATE TREATMENT BASED ON CNV STATUS
# ============================================================================
print("7. Updating treatment based on CNV status...")

# If CNV developed, 95% get anti-VEGF treatment
for i in range(N_PATIENTS):
    if data['cnv_developed'][i] == 'Yes' and np.random.random() < 0.95:
        data['treatment_approach'][i] = 'Anti-VEGF'

        # Choose agent (current practice patterns)
        data['anti_vegf_agent'][i] = np.random.choice(
            ['Eylea', 'Lucentis', 'Avastin'],
            p=[0.50, 0.30, 0.20]
        )

        # Number of injections (mean 5, range 1-12)
        data['number_of_injections'][i] = int(np.clip(
            np.random.gamma(2, 2.5, 1)[0], 1, 12
        ))

        # 8% get supplemental laser
        if np.random.random() < 0.08:
            data['supplemental_laser'][i] = 'Yes'

# ============================================================================
# TREATMENT RESPONSE (if treated)
# ============================================================================
print("8. Generating treatment response...")

# Response to treatment (if treated with anti-VEGF)
response_list = []
for i in range(N_PATIENTS):
    if data['treatment_approach'][i] == 'Anti-VEGF':
        # Better response with: more injections, Eylea/Lucentis vs Avastin
        good_prob = 0.50
        if data['number_of_injections'][i] >= 5:
            good_prob += 0.15
        if data['anti_vegf_agent'][i] in ['Eylea', 'Lucentis']:
            good_prob += 0.10

        if np.random.random() < good_prob:
            response_list.append('Good')
        elif np.random.random() < 0.65:
            response_list.append('Moderate')
        else:
            response_list.append('Poor')
    else:
        response_list.append('NA')

data['treatment_response'] = response_list

# ============================================================================
# FINAL VISUAL ACUITY
# ============================================================================
print("9. Generating final visual acuity...")

# Final VA depends on:
# - Baseline VA
# - CNV development (worse if CNV)
# - Treatment response (better if good response)
# - Foveal involvement (worse if involved)

final_va = np.array(data['baseline_va_logmar']).copy()

# CNV developed: +0.3 logMAR (worse) on average
for i in range(N_PATIENTS):
    if data['cnv_developed'][i] == 'Yes':
        final_va[i] += np.random.normal(0.3, 0.15)

        # Modify based on treatment response
        if data['treatment_response'][i] == 'Good':
            final_va[i] -= 0.25  # Improve
        elif data['treatment_response'][i] == 'Moderate':
            final_va[i] -= 0.10  # Slight improvement
        # Poor response: no change from CNV worsening
    else:
        # No CNV: Most stable or improve slightly
        final_va[i] += np.random.normal(-0.05, 0.10)

# Foveal involvement: Generally worse outcomes
foveal_mask = np.array(data['foveal_involvement']) == 'Yes'
final_va[foveal_mask] += 0.15

data['final_va_logmar'] = np.clip(final_va, 0.0, 2.5).round(2)

# ============================================================================
# FOLLOW-UP DURATION
# ============================================================================
print("10. Generating follow-up duration...")

# Follow-up duration (12-48 months, mean 24)
# Longer if CNV developed (need monitoring)
followup_mean = np.where(
    np.array(data['cnv_developed']) == 'Yes',
    30,  # Longer follow-up if CNV
    20   # Shorter if stable
)

data['follow_up_duration_months'] = np.clip(
    np.random.normal(followup_mean, 8, N_PATIENTS),
    6, 48
).round(1)

# Ensure time_to_cnv < follow_up duration
for i in range(N_PATIENTS):
    if data['cnv_developed'][i] == 'Yes':
        if data['time_to_cnv_months'][i] >= data['follow_up_duration_months'][i]:
            data['follow_up_duration_months'][i] = data['time_to_cnv_months'][i] + np.random.uniform(3, 12)

# ============================================================================
# CREATE DATAFRAME AND SAVE
# ============================================================================
print("\n" + "=" * 60)
print("Creating DataFrame...")

df = pd.DataFrame(data)

# Reorder columns logically
column_order = [
    # Demographics
    'patient_id', 'age', 'sex', 'race', 'occupation_risk',

    # Injury characteristics
    'mechanism_of_injury', 'rupture_location_clock_hours', 'rupture_length_mm',
    'distance_from_fovea_um', 'foveal_involvement', 'choroidal_thickness_um',
    'time_to_presentation_days', 'subretinal_hemorrhage',

    # Baseline OCT
    'baseline_cst_um', 'outer_retinal_disruption_score', 'rpe_disruption',
    'subfoveal_choroidal_thickness_um', 'subretinal_fluid', 'intraretinal_cysts',
    'ez_integrity_percent', 'elm_intact', 'oct_quality_score',

    # Visual acuity
    'baseline_va_logmar', 'final_va_logmar',

    # Treatment
    'treatment_approach', 'anti_vegf_agent', 'number_of_injections', 'supplemental_laser',

    # Outcomes
    'cnv_developed', 'time_to_cnv_months', 'cnv_type', 'treatment_response',
    'follow_up_duration_months'
]

df = df[column_order]

# Save to CSV
output_file = '/Users/makdjulbegovic/Desktop/Claude_Teach/choroidal_rupture_data.csv'
df.to_csv(output_file, index=False)

print(f"✓ Database saved to: {output_file}")
print(f"\nDatabase dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)
print(f"\nPatient Demographics:")
print(f"  Age: {df['age'].mean():.1f} ± {df['age'].std():.1f} years (range: {df['age'].min()}-{df['age'].max()})")
print(f"  Sex: {(df['sex'] == 'M').sum()} male ({(df['sex'] == 'M').sum()/len(df)*100:.1f}%), {(df['sex'] == 'F').sum()} female")

print(f"\nInjury Characteristics:")
print(f"  Rupture length: {df['rupture_length_mm'].mean():.2f} ± {df['rupture_length_mm'].std():.2f} mm")
print(f"  Foveal involvement: {(df['foveal_involvement'] == 'Yes').sum()} patients ({(df['foveal_involvement'] == 'Yes').sum()/len(df)*100:.1f}%)")
print(f"  Distance from fovea: {df['distance_from_fovea_um'].mean():.0f} ± {df['distance_from_fovea_um'].std():.0f} µm")

print(f"\nOutcomes:")
print(f"  CNV developed: {(df['cnv_developed'] == 'Yes').sum()} patients ({(df['cnv_developed'] == 'Yes').sum()/len(df)*100:.1f}%)")
print(f"  Mean time to CNV: {df['time_to_cnv_months'].mean():.1f} ± {df['time_to_cnv_months'].std():.1f} months")
print(f"  Patients treated with anti-VEGF: {(df['treatment_approach'] == 'Anti-VEGF').sum()}")

print(f"\nVisual Acuity:")
print(f"  Baseline VA: {df['baseline_va_logmar'].mean():.2f} ± {df['baseline_va_logmar'].std():.2f} logMAR")
print(f"  Final VA: {df['final_va_logmar'].mean():.2f} ± {df['final_va_logmar'].std():.2f} logMAR")

print("\n" + "=" * 60)
print("DATA PREVIEW (First 10 rows)")
print("=" * 60)
print(df.head(10).to_string())

print("\n" + "=" * 60)
print("COLUMN INFORMATION")
print("=" * 60)
print(df.info())

print("\n✓ Synthetic database generation complete!")
print(f"⚠️  REMINDER: This is SYNTHETIC data for educational purposes only")
