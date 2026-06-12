"""
Predictive Modeling for CNV Development After Choroidal Rupture
===============================================================

This script builds and validates predictive models:
1. Cox Proportional Hazards Model (time-to-event)
2. Random Forest Classifier (binary classification)

⚠️ SYNTHETIC DATA - For Educational Demonstration Only
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (roc_auc_score, roc_curve, confusion_matrix,
                             classification_report, accuracy_score)
import pickle
import warnings
warnings.filterwarnings('ignore')

# Try to import lifelines for Cox model
try:
    from lifelines import CoxPHFitter
    from lifelines.utils import concordance_index
    from lifelines import KaplanMeierFitter
    LIFELINES_AVAILABLE = True
except ImportError:
    print("⚠️  lifelines not installed. Installing now...")
    import subprocess
    subprocess.check_call(['pip', 'install', '-q', 'lifelines'])
    from lifelines import CoxPHFitter
    from lifelines.utils import concordance_index
    from lifelines import KaplanMeierFitter
    LIFELINES_AVAILABLE = True

print("=" * 70)
print("PREDICTIVE MODELING - CNV DEVELOPMENT AFTER CHOROIDAL RUPTURE")
print("=" * 70)

# ============================================================================
# LOAD AND PREPARE DATA
# ============================================================================
print("\n1. Loading and preparing data...")
df = pd.read_csv('/Users/makdjulbegovic/Desktop/Claude_Teach/choroidal_rupture_data.csv')
print(f"   ✓ Loaded {len(df)} patients")

# Create binary outcome
df['cnv_binary'] = (df['cnv_developed'] == 'Yes').astype(int)

# Create binary features
df['foveal_involvement_binary'] = (df['foveal_involvement'] == 'Yes').astype(int)
df['subretinal_hemorrhage_binary'] = (df['subretinal_hemorrhage'] == 'Yes').astype(int)
df['rpe_disruption_binary'] = (df['rpe_disruption'] == 'Yes').astype(int)
df['subretinal_fluid_binary'] = (df['subretinal_fluid'] == 'Yes').astype(int)
df['intraretinal_cysts_binary'] = (df['intraretinal_cysts'] == 'Yes').astype(int)
df['elm_intact_binary'] = (df['elm_intact'] == 'Yes').astype(int)
df['sex_binary'] = (df['sex'] == 'M').astype(int)

# Select predictor variables
predictors = [
    'age',
    'sex_binary',
    'rupture_length_mm',
    'distance_from_fovea_um',
    'foveal_involvement_binary',
    'choroidal_thickness_um',
    'subretinal_hemorrhage_binary',
    'baseline_cst_um',
    'outer_retinal_disruption_score',
    'rpe_disruption_binary',
    'ez_integrity_percent',
    'subretinal_fluid_binary',
    'intraretinal_cysts_binary',
    'baseline_va_logmar'
]

print(f"   ✓ Using {len(predictors)} predictor variables")

# ============================================================================
# COX PROPORTIONAL HAZARDS MODEL
# ============================================================================
print("\n2. BUILDING COX PROPORTIONAL HAZARDS MODEL")
print("=" * 70)

# Prepare data for Cox model
# For Cox model, we need: time, event, and predictors
# Use follow-up duration as censoring time for those without CNV
df_cox = df.copy()
df_cox['time'] = df_cox.apply(
    lambda row: row['time_to_cnv_months'] if pd.notna(row['time_to_cnv_months'])
    else row['follow_up_duration_months'],
    axis=1
)
df_cox['event'] = df_cox['cnv_binary']

# Create Cox model dataset
cox_data = df_cox[['time', 'event'] + predictors].copy()

# Remove any rows with missing data
cox_data = cox_data.dropna()
print(f"   Dataset: {len(cox_data)} patients")
print(f"   Events: {cox_data['event'].sum()} CNV cases")
print(f"   Censored: {len(cox_data) - cox_data['event'].sum()} cases")

# Fit Cox model
print("\n   Fitting Cox Proportional Hazards model...")
cph = CoxPHFitter(penalizer=0.01)  # Small L2 penalty for stability
cph.fit(cox_data, duration_col='time', event_col='event', show_progress=False)

print("\n   ✓ Model fitted successfully")
print(f"   Concordance index (C-index): {cph.concordance_index_:.3f}")

# Get hazard ratios
print("\n   Top Risk Factors (Hazard Ratios):")
print("   " + "-" * 66)
print(f"   {'Variable':<40} {'HR':<8} {'95% CI':<15} {'p-value'}")
print("   " + "-" * 66)

# Sort by absolute coefficient (log hazard ratio)
hr_df = cph.summary.copy()
hr_df['abs_coef'] = hr_df['coef'].abs()
hr_df = hr_df.sort_values('abs_coef', ascending=False)

# Create readable names
var_names = {
    'foveal_involvement_binary': 'Foveal involvement',
    'distance_from_fovea_um': 'Distance from fovea (per 100µm)',
    'outer_retinal_disruption_score': 'Outer retinal disruption',
    'rupture_length_mm': 'Rupture length (mm)',
    'ez_integrity_percent': 'EZ integrity (per 10%)',
    'baseline_va_logmar': 'Baseline VA (logMAR)',
    'rpe_disruption_binary': 'RPE disruption',
    'age': 'Age (years)',
    'subretinal_fluid_binary': 'Subretinal fluid',
    'baseline_cst_um': 'Baseline CST (per 10µm)',
    'subretinal_hemorrhage_binary': 'Subretinal hemorrhage',
    'choroidal_thickness_um': 'Choroidal thickness (per 10µm)',
    'intraretinal_cysts_binary': 'Intraretinal cysts',
    'sex_binary': 'Male sex'
}

for idx, row in hr_df.head(10).iterrows():
    var_name = var_names.get(idx, idx)
    hr = np.exp(row['coef'])
    ci_lower = np.exp(row['coef'] - 1.96 * row['se(coef)'])
    ci_upper = np.exp(row['coef'] + 1.96 * row['se(coef)'])
    p_val = row['p']

    p_str = '<0.001' if p_val < 0.001 else f'{p_val:.3f}'
    print(f"   {var_name:<40} {hr:<8.2f} ({ci_lower:.2f}-{ci_upper:.2f})  {p_str}")

# Save Cox model
with open('/Users/makdjulbegovic/Desktop/Claude_Teach/cox_model.pkl', 'wb') as f:
    pickle.dump(cph, f)
print("\n   ✓ Cox model saved to: cox_model.pkl")

# ============================================================================
# RANDOM FOREST MODEL
# ============================================================================
print("\n\n3. BUILDING RANDOM FOREST CLASSIFIER")
print("=" * 70)

# Prepare data for Random Forest
X = df[predictors].copy()
y = df['cnv_binary'].copy()

# Remove any rows with missing data
valid_idx = ~X.isnull().any(axis=1)
X = X[valid_idx]
y = y[valid_idx]

print(f"   Dataset: {len(X)} patients")
print(f"   CNV cases: {y.sum()} ({y.sum()/len(y)*100:.1f}%)")

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Training set: {len(X_train)} patients")
print(f"   Test set: {len(X_test)} patients")

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest
print("\n   Training Random Forest model...")
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train_scaled, y_train)
print("   ✓ Model trained successfully")

# ============================================================================
# MODEL EVALUATION
# ============================================================================
print("\n4. MODEL EVALUATION")
print("=" * 70)

# Predictions
y_pred_train = rf.predict(X_train_scaled)
y_pred_test = rf.predict(X_test_scaled)
y_pred_proba_test = rf.predict_proba(X_test_scaled)[:, 1]

# Training performance
train_acc = accuracy_score(y_train, y_pred_train)
print(f"\n   Training set performance:")
print(f"   Accuracy: {train_acc:.3f}")

# Test performance
test_acc = accuracy_score(y_test, y_pred_test)
test_auc = roc_auc_score(y_test, y_pred_proba_test)

print(f"\n   Test set performance:")
print(f"   Accuracy: {test_acc:.3f}")
print(f"   AUC-ROC: {test_auc:.3f}")

# Classification report
print("\n   Classification Report (Test Set):")
print("   " + "-" * 66)
report = classification_report(y_test, y_pred_test, target_names=['No CNV', 'CNV'], digits=3)
for line in report.split('\n'):
    if line.strip():
        print("   " + line)

# Confusion matrix
cm = confusion_matrix(y_test, y_pred_test)
print("\n   Confusion Matrix (Test Set):")
print("   " + "-" * 40)
print(f"                Predicted No    Predicted CNV")
print(f"   Actual No        {cm[0,0]:<15} {cm[0,1]:<15}")
print(f"   Actual CNV       {cm[1,0]:<15} {cm[1,1]:<15}")

# Sensitivity and specificity
sensitivity = cm[1,1] / (cm[1,1] + cm[1,0])
specificity = cm[0,0] / (cm[0,0] + cm[0,1])
ppv = cm[1,1] / (cm[1,1] + cm[0,1])
npv = cm[0,0] / (cm[0,0] + cm[1,0])

print(f"\n   Sensitivity (Recall): {sensitivity:.3f}")
print(f"   Specificity: {specificity:.3f}")
print(f"   Positive Predictive Value: {ppv:.3f}")
print(f"   Negative Predictive Value: {npv:.3f}")

# Cross-validation
print("\n   5-Fold Cross-Validation on Full Dataset:")
cv_scores = cross_val_score(rf, X, y, cv=5, scoring='roc_auc')
print(f"   Mean AUC: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
print(f"   Range: {cv_scores.min():.3f} - {cv_scores.max():.3f}")

# ============================================================================
# FEATURE IMPORTANCE
# ============================================================================
print("\n\n5. FEATURE IMPORTANCE ANALYSIS")
print("=" * 70)

# Get feature importance
feature_importance = pd.DataFrame({
    'feature': predictors,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("\n   Top 10 Most Important Features:")
print("   " + "-" * 50)
print(f"   {'Feature':<40} {'Importance'}")
print("   " + "-" * 50)

for idx, row in feature_importance.head(10).iterrows():
    var_name = var_names.get(row['feature'], row['feature'])
    print(f"   {var_name:<40} {row['importance']:.4f}")

# Save feature importance
feature_importance.to_csv('/Users/makdjulbegovic/Desktop/Claude_Teach/feature_importance.csv', index=False)

# ============================================================================
# SAVE MODELS AND SCALERS
# ============================================================================
print("\n\n6. SAVING MODELS")
print("=" * 70)

# Save Random Forest model
with open('/Users/makdjulbegovic/Desktop/Claude_Teach/rf_model.pkl', 'wb') as f:
    pickle.dump(rf, f)
print("   ✓ Random Forest model saved to: rf_model.pkl")

# Save scaler
with open('/Users/makdjulbegovic/Desktop/Claude_Teach/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("   ✓ Scaler saved to: scaler.pkl")

# Save feature list
with open('/Users/makdjulbegovic/Desktop/Claude_Teach/feature_list.pkl', 'wb') as f:
    pickle.dump(predictors, f)
print("   ✓ Feature list saved to: feature_list.pkl")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n" + "=" * 70)
print("MODEL SUMMARY")
print("=" * 70)

print("\n📊 Cox Proportional Hazards Model:")
print(f"   C-index: {cph.concordance_index_:.3f}")
print(f"   Top risk factors:")
top_3_hr = hr_df.head(3)
for idx, row in top_3_hr.iterrows():
    var_name = var_names.get(idx, idx)
    hr = np.exp(row['coef'])
    print(f"     - {var_name}: HR = {hr:.2f}")

print("\n📊 Random Forest Model:")
print(f"   Test AUC: {test_auc:.3f}")
print(f"   Test Accuracy: {test_acc:.3f}")
print(f"   Sensitivity: {sensitivity:.3f}")
print(f"   Specificity: {specificity:.3f}")
print(f"   Top predictors:")
for idx, row in feature_importance.head(3).iterrows():
    var_name = var_names.get(row['feature'], row['feature'])
    print(f"     - {var_name}: {row['importance']:.3f}")

print("\n" + "=" * 70)
print("✓ Predictive modeling complete!")
print("   Models ready for deployment in web app")
print("=" * 70)
