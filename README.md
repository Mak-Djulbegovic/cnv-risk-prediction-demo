# AI for Ophthalmology Research: CNV Prediction Demo
## Presentation Materials for Ophthalmology Residents

⚠️ **IMPORTANT: This is SYNTHETIC DATA for educational demonstration only. NOT for clinical use.**

---

## Overview

This package contains a complete demonstration of agentic AI systems for ophthalmology research, specifically predicting choroidal neovascularization (CNV) development after traumatic choroidal rupture.

**What's Included:**
- Synthetic dataset (1000 patients, 33 variables)
- Exploratory data analysis
- Predictive models (Cox PH + Random Forest)
- Publication-quality visualizations
- Interactive web application
- PowerPoint presentation

---

## Quick Start Guide

### 1. View the Presentation Outline
```bash
open presentation_outline.md
```

### 2. Generate the Database
```bash
python generate_synthetic_data.py
```
**Output:** `choroidal_rupture_data.csv` (1000 rows × 33 columns)

### 3. Run Exploratory Analysis
```bash
python exploratory_analysis.py
```
**Output:** Summary statistics and univariate analysis

### 4. Build Predictive Models
```bash
python predictive_modeling.py
```
**Output:**
- `cox_model.pkl` - Cox proportional hazards model
- `rf_model.pkl` - Random Forest classifier
- `scaler.pkl` - Feature scaler
- `feature_list.pkl` - List of predictors

### 5. Create Visualizations
```bash
python create_visualizations.py
```
**Output:** 7 publication-quality figures (PNG, 300 DPI)

### 6. Launch Web App
```bash
./run_app.sh
```
**Or manually:**
```bash
streamlit run cnv_prediction_app.py
```

The app will open in your web browser at `http://localhost:8501`

---

## File Structure

```
Claude_Teach/
│
├── README.md                          # This file
├── presentation_outline.md            # Detailed presentation structure
│
├── DATA GENERATION
│   ├── generate_synthetic_data.py     # Creates 1000-patient database
│   └── choroidal_rupture_data.csv     # Output dataset
│
├── ANALYSIS
│   ├── exploratory_analysis.py        # Descriptive statistics
│   └── summary_table1.csv             # Summary table output
│
├── MODELING
│   ├── predictive_modeling.py         # Cox PH + Random Forest
│   ├── cox_model.pkl                  # Saved Cox model
│   ├── rf_model.pkl                   # Saved Random Forest
│   ├── scaler.pkl                     # Feature scaler
│   ├── feature_list.pkl               # Predictor variables
│   └── feature_importance.csv         # Feature importance table
│
├── VISUALIZATIONS
│   ├── create_visualizations.py       # Generate all figures
│   ├── figure1_kaplan_meier.png       # Survival curves
│   ├── figure2_feature_importance.png # Top predictors
│   ├── figure3_roc_curve.png          # Model performance
│   ├── figure4_risk_stratification.png# Risk groups
│   ├── figure5_correlation_heatmap.png# Variable correlations
│   ├── figure6_cnv_by_age.png         # CNV by age group
│   └── figure7_treatment_response.png # Treatment outcomes
│
├── WEB APP
│   ├── cnv_prediction_app.py          # Streamlit application
│   └── run_app.sh                     # App launcher script
│
└── PRESENTATION
    └── [PowerPoint file will go here]
```

---

## Presentation Flow (28-33 minutes)

### Phase 1: Introduction (5 min)
- Disclosures
- LLM → Agentic systems evolution
- Available AI models (focus on Claude)

### Phase 2: Framework (4 min)
- 4-C Prompt Engineering Framework:
  1. **Context** - Set the stage
  2. **Clear Goal** - What you want
  3. **Constraints** - Specifications
  4. **Collaboration** - Iterate
- Demonstrate agentic autonomy

### Phase 3: LIVE DEMO (15-18 min)
Show the complete pipeline:

**A. Data Generation (5 min)**
```bash
python generate_synthetic_data.py
```
- Show: 1000 rows × 33 columns
- Display first 10-20 rows
- Emphasize depth and realism

**B. Exploratory Analysis (4 min)**
```bash
python exploratory_analysis.py
```
- Descriptive statistics
- Risk factor identification

**C. Predictive Modeling (4 min)**
```bash
python predictive_modeling.py
```
- Cox model: C-index = 0.662
- Random Forest: AUC = 0.768
- Feature importance

**D. Visualization (2 min)**
```bash
python create_visualizations.py
```
- 7 publication-quality figures in seconds

**E. Web App (3-4 min)**
```bash
./run_app.sh
```
- Launch interactive tool
- Demo 2 patient cases:
  - Low-risk patient
  - High-risk patient

### Phase 4: Code Review (2 min)
- Show screenshots of agent-generated code
- Emphasize autonomy

### Phase 5: Results & Discussion (3 min)
- Top risk factors
- Model performance
- Clinical implications

### Phase 6: Wrap-up (5-8 min)
- Other use cases
- Practical tips
- Resources
- Q&A

---

## Demo Patient Cases for Web App

### Case 1: Low-Risk Patient
- Age: 65 years
- Sex: Male
- Rupture length: 1.5 mm
- Distance from fovea: 2500 µm
- Foveal involvement: No
- Outer retinal disruption: Mild (1)
- EZ integrity: 85%
- Baseline VA: 0.3 logMAR (~20/40)

**Expected Output:** ~15-25% CNV risk

### Case 2: High-Risk Patient
- Age: 28 years
- Sex: Male
- Rupture length: 6.0 mm
- Distance from fovea: 200 µm
- Foveal involvement: Yes
- Outer retinal disruption: Severe (3)
- EZ integrity: 20%
- Baseline VA: 1.0 logMAR (~20/200)
- Subretinal hemorrhage: Yes
- RPE disruption: Yes

**Expected Output:** ~75-85% CNV risk

---

## Key Messages for Presentation

1. **Agentic systems work autonomously**
   - You prompt, they execute end-to-end
   - Not just Q&A - they write code, run analysis, create tools

2. **From question to clinical tool in one session**
   - Database → Analysis → Model → Web App
   - All with natural language prompts

3. **Research-grade outputs**
   - 1000 patients, 33 variables
   - Publication-quality analysis
   - Deployable applications

4. **Augmentation, not replacement**
   - You guide with domain knowledge
   - Agent handles technical execution
   - You verify and validate

5. **Accessible to everyone**
   - No coding background required
   - Transparent: see what was built
   - Learn from generated code

6. **Available NOW**
   - These tools exist today
   - Start simple, build complexity
   - Iterate and improve

---

## Technical Requirements

### Software Dependencies
```bash
# Install required packages
pip install pandas numpy matplotlib seaborn scikit-learn lifelines streamlit
```

### Minimum Requirements
- Python 3.8+
- 4GB RAM
- Modern web browser (for Streamlit app)

---

## Troubleshooting

### Issue: Models not loading in web app
**Solution:** Ensure all `.pkl` files are in the same directory as `cnv_prediction_app.py`

### Issue: Streamlit won't start
**Solution:**
```bash
pip install --upgrade streamlit
streamlit run cnv_prediction_app.py
```

### Issue: Figures not generating
**Solution:** Check that matplotlib and seaborn are installed:
```bash
pip install matplotlib seaborn
```

---

## Dataset Variables (33 total)

### Demographics (5)
- patient_id, age, sex, race, occupation_risk

### Injury Characteristics (8)
- mechanism_of_injury, rupture_location_clock_hours, rupture_length_mm
- distance_from_fovea_um, foveal_involvement, choroidal_thickness_um
- time_to_presentation_days, subretinal_hemorrhage

### Baseline OCT (9)
- baseline_cst_um, outer_retinal_disruption_score, rpe_disruption
- subfoveal_choroidal_thickness_um, subretinal_fluid, intraretinal_cysts
- ez_integrity_percent, elm_intact, oct_quality_score

### Visual Acuity (2)
- baseline_va_logmar, final_va_logmar

### Treatment (4)
- treatment_approach, anti_vegf_agent, number_of_injections, supplemental_laser

### Outcomes (5)
- cnv_developed, time_to_cnv_months, cnv_type, treatment_response, follow_up_duration_months

---

## Model Performance Summary

### Cox Proportional Hazards Model
- **C-index:** 0.662 (good discrimination)
- **Top risk factors:**
  - Foveal involvement (HR = 1.79)
  - Outer retinal disruption (HR = 1.18)
  - Rupture length (HR = 1.06 per mm)

### Random Forest Classifier
- **AUC:** 0.768
- **Accuracy:** 0.735
- **Sensitivity:** 0.850 (catches 85% of CNV cases)
- **Specificity:** 0.534
- **Top predictors:**
  - Distance from fovea (importance = 0.179)
  - Baseline VA (importance = 0.158)
  - Foveal involvement (importance = 0.116)

---

## Literature References

This synthetic dataset is based on published literature:

1. Ament CS, et al. *Ophthalmology.* 2006 - CNV incidence ~20-30% post-rupture
2. Gross NE, et al. *Retina.* 2001 - Risk factors for CNV development
3. Gass JD. *Arch Ophthalmol.* 1987 - Natural history of choroidal rupture

---

## Contact & Feedback

For questions or feedback about this demonstration:
- Built with Claude Code (Anthropic)
- Demonstration created: 2026
- Educational use only

---

## License & Disclaimer

**⚠️ IMPORTANT DISCLAIMERS:**

1. **SYNTHETIC DATA ONLY:** All data in this demonstration is computer-generated and does not represent real patients.

2. **NOT FOR CLINICAL USE:** This tool is for educational and research demonstration purposes only. Do not use for clinical decision-making.

3. **NO MEDICAL ADVICE:** This software does not provide medical advice. All clinical decisions should be made by qualified healthcare professionals.

4. **RESEARCH ONLY:** Models are trained on synthetic data and have not been validated on real patient data.

5. **EDUCATIONAL PURPOSE:** This demonstration is designed to teach residents about AI capabilities in research, not to replace clinical judgment.

---

## Next Steps for Real Implementation

To adapt this workflow for real clinical research:

1. **Use real data** (with IRB approval and proper de-identification)
2. **Validate models** on independent test sets
3. **External validation** on different patient populations
4. **Clinical trial** to assess real-world performance
5. **Regulatory approval** if intended for clinical use
6. **Continuous monitoring** and model updates

---

**Built with Claude Code - Demonstrating the power of agentic AI systems for medical research**

🤖 From research question to clinical tool in one session
