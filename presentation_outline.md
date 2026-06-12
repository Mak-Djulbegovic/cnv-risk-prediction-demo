# AI for Ophthalmology Research: From LLMs to Agentic Systems
## Presentation Outline (20-30 minutes, Interactive)

---

## SLIDE 1: Title Slide
- **Title:** AI-Powered Research in Ophthalmology: Agentic Systems in Action
- **Subtitle:** Streamlining Data Analysis and Clinical Research
- **Visual:** Simple eye/retina illustration or abstract neural network overlay

---

## SLIDE 2: Disclosures
- **Content:** No disclosures
- **Note:** Keep it clean and simple

---

## SLIDE 3: The AI Landscape
- **Title:** Many AI Models Available
- **Visual:** Logos or names of major models
  - GPT-4, Gemini, Claude, Llama, etc.
- **Content:**
  - "Today we're focusing on Claude"
  - "Why? Most experience, strong reasoning, excellent for research"
- **Keep it brief:** 1-2 bullet points max

---

## SLIDE 4: The Evolution - LLMs to Agentic Systems
- **Title:** From Chatbots to Autonomous Agents
- **Visual:** Simple progression diagram

**Two columns:**

**Traditional LLMs (2023)**
- Single query → single response
- No memory between tasks
- Manual copy-paste workflow
- You do the work

**Agentic Systems (2024-2025)**
- Multi-step autonomous problem solving
- Uses tools (code, search, files)
- Remembers context and iterates
- AI does the work

**Key Point:** "Like having a research assistant who can code, analyze data, and create visualizations"

---

## SLIDE 5: What Can Agentic Systems Do?
- **Title:** Capabilities for Research
- **Visual:** Icon-based layout

**Four quadrants:**
1. **Data Generation & Simulation**
   - Create synthetic datasets
   - Design study protocols

2. **Statistical Analysis**
   - Run complex models
   - Survival analysis, regression, ML

3. **Visualization**
   - Create publication-quality figures
   - Interactive dashboards

4. **Literature Integration**
   - Search and summarize papers
   - Evidence-based parameter selection

---

## SLIDE 6: Prompt Engineering for Agentic Systems
- **Title:** How to Talk to AI Agents
- **Framework for effective prompts:**

**The 4-C Framework:**
1. **Context** - Set the stage
   - "I'm studying choroidal rupture outcomes"
   - "I need to present findings to residents"

2. **Clear Goal** - What you want
   - "Create a database of 1000 patients"
   - "Build a predictive model for CNV development"

3. **Constraints** - Specifications
   - "Include 25 clinically relevant variables"
   - "Use literature-based parameters"
   - "Generate publication-quality figures"

4. **Collaboration** - Iterate
   - "Show me the data structure first"
   - "Let's add this variable based on reviewer feedback"

- **Key Point:** Agentic systems use tools autonomously - you guide, they execute
- **Visual:** Example prompt → Agent actions (reads papers → writes code → runs analysis → creates plots)

---

## SLIDE 7: Today's Demo
- **Title:** Real-World Use Case
- **Clinical Scenario:**
  - "Predicting neovascularization after traumatic choroidal rupture"
  - Key question: How long until CNV develops?
  - **⚠️ DISCLOSURE: Synthetic data for educational demonstration**

- **What we'll show:**
  1. Generate synthetic patient database (1000 patients, 25+ variables)
  2. Explore the data structure and depth
  3. Build predictive model
  4. Analyze risk factors
  5. Create visualizations
  6. Build interactive web app
  7. All done live with Claude Code as autonomous agent

- **Interactive element:** "What variables would YOU include in this study?"
  - Take 2-3 suggestions from audience
  - Show how to incorporate them into the prompt

---

## SLIDE 8: [LIVE DEMO SECTION]
- **Title:** Building the Study - Live
- **This slide stays on screen during demo**
- **What we demonstrate:**

  **Phase 1: Data Creation (5 min)**
  - **Prompt shown:** "Create a synthetic database of 1000 patients with traumatic choroidal rupture..."
  - **Agent actions:** Claude Code autonomously:
    - Searches literature for realistic parameters
    - Writes Python script to generate data
    - Creates CSV with proper distributions
  - **Show the data:**
    - Database dimensions: 1000 rows × 25-30 columns
    - Display first 10-20 rows in terminal/Pandas
    - Show column list and data types
    - Sample statistics (means, ranges)
  - **Capture screenshot** of data generation code

  **Phase 2: Exploratory Analysis (5 min)**
  - **Prompt:** "Analyze this dataset, show descriptive statistics and correlations"
  - **Agent autonomously:**
    - Loads data, checks for missing values
    - Generates summary statistics
    - Creates correlation matrices
    - Kaplan-Meier survival curves
  - **Capture screenshot** of analysis code
  - Show output tables and initial plots

  **Phase 3: Predictive Modeling (5 min)**
  - **Prompt:** "Build a Cox model and Random Forest to predict time to CNV"
  - **Agent autonomously:**
    - Preprocesses data, handles categorical variables
    - Trains multiple models
    - Validates with cross-validation
    - Generates feature importance
  - **Capture screenshot** of modeling code
  - Show model performance metrics

  **Phase 4: Visualization (3 min)**
  - **Prompt:** "Create publication-quality figures"
  - **Agent creates:**
    - Survival curves by risk group
    - Feature importance plots
    - ROC curves
  - **Capture screenshot** of plotting code

  **Phase 5: Build Clinical Tool (3-4 min)**
  - **Prompt:** "Build a web app where I can input patient data and get CNV risk prediction"
  - **Agent autonomously:**
    - Creates Streamlit/Gradio app
    - Loads trained model
    - Builds input interface
    - Generates prediction output
  - **Capture screenshot** of app code
  - **Launch app and demo live**

---

## SLIDE 9: The Clinical Tool - LIVE DEMO
- **Title:** From Model to Application
- **LIVE INTERACTION with the web app:**
  - Show the interface running locally
  - **Demo Case 1:** Low-risk patient
    - 65-year-old, small peripheral rupture, no foveal involvement
    - Enter parameters → Get prediction
    - Show: "15% risk of CNV at 12 months"

  - **Demo Case 2:** High-risk patient
    - 28-year-old, large rupture involving fovea, significant subretinal hemorrhage
    - Enter parameters → Get prediction
    - Show: "75% risk of CNV at 12 months"

  - **Show output includes:**
    - Risk probability with confidence interval
    - Top contributing risk factors
    - Survival curve for this patient profile
    - Downloadable report

- **Emphasize:** "From research question to clinical decision tool - all in one session with an agentic system"
- **Visual:** Live web app + code screenshot showing how agent built it

---

## SLIDE 10: Behind the Scenes - The Code
- **Title:** What Did the Agent Actually Do?
- **Show screenshots of the generated code:**
  - **Data generation script** (10-15 lines highlighted)
  - **Analysis code** (key functions highlighted)
  - **Modeling code** (model training section)
  - **Web app code** (Streamlit interface)

- **Key points:**
  - "You didn't write this - the agent did"
  - "All based on natural language prompts"
  - "Code is readable, well-commented, publication-ready"
  - "You can modify and extend it"

- **Emphasize autonomy:** Agent chose libraries, wrote functions, handled errors, iterated on its own

---

## SLIDE 11: Results Overview
- **Title:** What Did We Learn?
- **Display key findings from the demo:**
  - Top 3 risk factors for CNV development
  - Median time to neovascularization
  - Model performance (C-statistic, AUC)
  - Visual: 1-2 key plots from analysis

- **Interactive:** "How could this change clinical practice?"

---

## SLIDE 12: Other Use Cases
- **Title:** Beyond This Example
- **Quick examples (bullet points + icons):**
  - Systematic reviews & meta-analyses
  - Clinical trial design & power calculations
  - Image analysis pipelines (OCT, fundus photos)
  - Grant writing & literature searches
  - Patient cohort identification from EHR
  - Teaching case generation
  - Custom clinical calculators and tools

---

## SLIDE 13: Practical Tips
- **Title:** Getting Started with Agentic Systems
- **Content:**
  1. **Start with clear prompts** - Use the 4-C framework
  2. **Let the agent work autonomously** - Don't micromanage
  3. **Iterate with feedback** - "Now add X variable" or "Make this figure better"
  4. **Verify outputs** - AI can make mistakes, check the logic
  5. **Use for hypothesis generation** - Not final conclusions without review
  6. **Best for:** Data exploration, visualization, preliminary analysis, tool building

- **What it's NOT:**
  - Replacement for statistical consultation on final analysis
  - Ready for publication without human verification
  - Substitute for domain expertise

---

## SLIDE 14: Hands-On Time (If time permits)
- **Title:** Your Turn
- **Interactive exercise:**
  - "Think of a research question in your field"
  - "We'll show you how to start the analysis with Claude Code"
  - Take 1-2 volunteer questions
  - Quick 2-3 minute demo for each
  - Audience sees the agentic workflow in real-time

---

## SLIDE 15: Resources & Next Steps
- **Title:** Continue Learning
- **Content:**
  - **Claude.ai** - Free tier available for chat
  - **Claude Code CLI** - For agentic development workflows
  - **Cursor, Windsurf** - AI-powered coding environments
  - **Important considerations:**
    - Review institutional guidelines on AI use
    - HIPAA compliance for real patient data
    - Data privacy and security
    - IRB requirements for AI-assisted research

---

## SLIDE 16: Questions & Discussion
- **Simple slide:** "Questions & Discussion"
- **Visual:** Keep it clean

---

## TECHNICAL SETUP BEFORE PRESENTATION:

### Pre-built Components:
1. **Synthetic Database Script** - Ready to run, generates data in ~30 seconds
2. **Analysis Pipeline** - Modular, can run step-by-step or all at once
3. **Web App** - Streamlit/Gradio app ready to launch
4. **Backup Results** - In case live demo fails, have pre-generated outputs
5. **Code Screenshots** - Capture key snippets during prep for PowerPoint slides
6. **Database Preview** - Have command ready to show df.head(), df.shape, df.info()

### What to Demonstrate Live:
- **Show database depth:** Run commands to display 1000 rows × 25-30 columns
- **Show raw data:** First 10-20 rows in terminal to show realistic values
- **Capture screenshots:** Take screenshots of each code file generated by agent
- **Launch web app:** Have it running on localhost, demo with real inputs
- **Emphasize autonomy:** Narrate what the agent is doing autonomously at each step

### Synthetic Data Disclosure:
- **Add to every relevant slide:** "⚠️ SYNTHETIC DATA - For Educational Demonstration"
- Include in title slide notes
- Mention verbally when showing database
- Include in any exported figures/results

### Variables for Database (20-30 variables):

**Demographics (5):**
- Age, Sex, Race, Occupation, Baseline health status

**Injury Characteristics (8):**
- Mechanism of injury, Rupture location (clock hours), Rupture length (mm)
- Distance from fovea (μm), Involvement of fovea (Y/N)
- Associated choroidal thickness, Time from injury to presentation
- Presence of subretinal hemorrhage

**Baseline OCT Parameters (8):**
- Central subfield thickness (μm), Outer retinal disruption (score 0-3)
- RPE disruption (Y/N), Subfoveal choroidal thickness
- Presence of subretinal fluid, Intraretinal cysts
- Ellipsoid zone integrity (%), External limiting membrane integrity

**Treatment (4):**
- Observation vs. intervention, Anti-VEGF if treated (Lucentis/Eylea/Avastin)
- Number of injections, Supplemental laser (Y/N)

**Outcomes (5):**
- Time to CNV development (months), Final visual acuity
- Need for treatment, CNV type (classic/occult/mixed)
- Response to treatment

### Literature-Based Parameters:
- CNV incidence: ~20-30% post choroidal rupture (cite appropriate papers)
- Mean time to CNV: 6-12 months
- Risk factors: Foveal involvement, larger rupture size, younger age

---

## PRESENTATION FLOW TIMING:

- Introduction & context (Slides 1-4): **5 minutes**
- Capabilities overview (Slide 5): **2 minutes**
- **Prompt engineering framework (Slide 6): **2 minutes**
- Demo setup (Slide 7): **2 minutes**
- **LIVE DEMO (Slide 8): **15-18 minutes**
  - Data creation + showing database structure: 5 min
  - Exploratory analysis: 4 min
  - Predictive modeling: 4 min
  - Visualization: 2 min
  - Build web app: 3-4 min
- **LIVE web app demo (Slide 9): **3 minutes** (two patient cases)
- Code review - what agent built (Slide 10): **2 minutes**
- Results & discussion (Slides 11-12): **3 minutes**
- Practical tips (Slide 13): **2 minutes**
- Optional hands-on (Slide 14): **3-5 minutes** (if time)
- Resources & Q&A (Slides 15-16): **3-5 minutes**

**Total: 28-33 minutes** (flexible with optional hands-on section)

**NOTE:** All demos are LIVE - showing the agentic system working in real-time, not pre-recorded

---

## INTERACTIVE ELEMENTS THROUGHOUT:

1. **Slide 6:** Audience suggests variables to include
2. **Slide 7:** Live demonstration with narration
3. **Slide 8:** Discuss clinical implications
4. **Slide 11:** Volunteer questions (if time)
5. **Throughout:** Encourage questions

---

## KEY MESSAGING:

1. **Agentic systems work autonomously** - You prompt, they execute end-to-end
   - Not just answering questions - writing code, running analysis, creating tools
   - Emphasis: "You focus on research questions, agent handles implementation"

2. **From question to clinical tool in one session**
   - Database → Analysis → Model → Web App
   - All with natural language prompts

3. **Show the depth** - Real research-grade outputs
   - 1000 patients, 25-30 variables (show the data!)
   - Publication-quality analysis
   - Deployable applications

4. **Not replacement for expertise** - Augmentation and acceleration
   - You guide with domain knowledge
   - Agent handles technical execution
   - You verify and validate outputs

5. **Accessible to everyone** - No coding background required
   - But outputs code you can learn from and modify
   - Transparent: see what the agent built (screenshots!)

6. **Practical applications NOW** - Not future tech
   - These tools are available today
   - Start with simple questions, build complexity
   - Iterate and improve with feedback
