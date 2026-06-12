"""
Create Visual Assets for Presentation
=====================================

Creates supporting images and code screenshots for the presentation.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import seaborn as sns

print("Creating supporting visual assets...")

# Set style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# ============================================================================
# 1. WORKFLOW DIAGRAM
# ============================================================================
print("\n1. Creating workflow diagram...")

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# Colors
color_prompt = '#3498DB'
color_agent = '#E74C3C'
color_output = '#2ECC71'

# Step 1: Prompt
step1_box = FancyBboxPatch((0.5, 4.5), 1.8, 1, boxstyle="round,pad=0.1",
                           edgecolor=color_prompt, facecolor=color_prompt, linewidth=3)
ax.add_patch(step1_box)
ax.text(1.4, 5, 'Natural\nLanguage\nPrompt', ha='center', va='center',
        fontsize=12, fontweight='bold', color='white')

# Arrow 1
ax.arrow(2.5, 5, 0.8, 0, head_width=0.2, head_length=0.15, fc=color_agent, ec=color_agent, linewidth=2)

# Step 2: Agent Processing
agent_box = FancyBboxPatch((3.5, 3.5), 2.5, 2, boxstyle="round,pad=0.1",
                          edgecolor=color_agent, facecolor=color_agent, linewidth=3)
ax.add_patch(agent_box)
ax.text(4.75, 5, '🤖 Claude Code', ha='center', va='top',
        fontsize=14, fontweight='bold', color='white')
ax.text(4.75, 4.5, 'Autonomous\nExecution', ha='center', va='center',
        fontsize=11, color='white')

# Sub-processes
sub_y = 3.8
for process in ['Write Code', 'Run Analysis', 'Create Outputs']:
    ax.text(4.75, sub_y, f'• {process}', ha='center', va='center',
            fontsize=9, color='white', style='italic')
    sub_y -= 0.35

# Arrow 2
ax.arrow(6.2, 4.5, 0.8, 0, head_width=0.2, head_length=0.15, fc=color_output, ec=color_output, linewidth=2)

# Step 3: Outputs
output_box = FancyBboxPatch((7.2, 2), 2.3, 3.5, boxstyle="round,pad=0.1",
                           edgecolor=color_output, facecolor=color_output, linewidth=3)
ax.add_patch(output_box)
ax.text(8.35, 5.1, 'Complete\nDeliverables', ha='center', va='center',
        fontsize=12, fontweight='bold', color='white')

outputs = ['📊 Database', '📈 Analysis', '🤖 Models', '📉 Figures', '🌐 Web App']
out_y = 4.3
for output in outputs:
    ax.text(8.35, out_y, output, ha='center', va='center',
            fontsize=10, color='white')
    out_y -= 0.5

# Title
ax.text(5, 0.5, 'Agentic AI Workflow: From Prompt to Product', ha='center', va='center',
        fontsize=16, fontweight='bold')

plt.tight_layout()
plt.savefig('workflow_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
print("   ✓ Saved: workflow_diagram.png")
plt.close()

# ============================================================================
# 2. DATABASE PREVIEW IMAGE
# ============================================================================
print("2. Creating database preview...")

# Load actual data
df = pd.read_csv('choroidal_rupture_data.csv')

# Create figure showing database structure
fig, ax = plt.subplots(figsize=(14, 6))
ax.axis('off')

# Title
ax.text(0.5, 0.95, 'Synthetic Database: First 5 Patients',
        transform=ax.transAxes, ha='center', fontsize=16, fontweight='bold')

# Show first 5 rows, select key columns
display_cols = ['patient_id', 'age', 'sex', 'rupture_length_mm', 'foveal_involvement',
                'baseline_va_logmar', 'cnv_developed', 'time_to_cnv_months']
df_display = df[display_cols].head(5)

# Create table
table_data = []
table_data.append(display_cols)
for idx, row in df_display.iterrows():
    table_data.append([str(row[col]) for col in display_cols])

table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                bbox=[0.05, 0.3, 0.9, 0.6])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)

# Style header
for i in range(len(display_cols)):
    cell = table[(0, i)]
    cell.set_facecolor('#3498DB')
    cell.set_text_props(weight='bold', color='white')

# Style data rows
for i in range(1, len(table_data)):
    for j in range(len(display_cols)):
        cell = table[(i, j)]
        cell.set_facecolor('#ECF0F1' if i % 2 == 0 else 'white')

# Add info box
info_text = f"Total: {len(df)} patients × {len(df.columns)} variables\nCNV Rate: {(df['cnv_developed']=='Yes').sum()/len(df)*100:.1f}%"
ax.text(0.5, 0.15, info_text, transform=ax.transAxes, ha='center',
        fontsize=11, bbox=dict(boxstyle='round', facecolor='#2ECC71', alpha=0.8),
        color='white', fontweight='bold')

plt.savefig('database_preview.png', dpi=300, bbox_inches='tight', facecolor='white')
print("   ✓ Saved: database_preview.png")
plt.close()

# ============================================================================
# 3. CODE EXAMPLE IMAGE
# ============================================================================
print("3. Creating code example image...")

fig, ax = plt.subplots(figsize=(12, 7))
ax.axis('off')

# Background
bg = Rectangle((0, 0), 1, 1, transform=ax.transAxes,
               facecolor='#1E1E1E', zorder=0)
ax.add_patch(bg)

# Code example
code_text = """# Data Generation - Agent-Written Code
import pandas as pd
import numpy as np

# Generate 1000 patients with choroidal rupture
N_PATIENTS = 1000

data = {
    'patient_id': [f'CR{str(i).zfill(4)}' for i in range(1, N_PATIENTS + 1)],
    'age': np.clip(np.random.normal(35, 15, N_PATIENTS).astype(int), 10, 85),
    'rupture_length_mm': np.clip(np.random.gamma(2, 1.5, N_PATIENTS), 0.5, 12.0),
    'foveal_involvement': np.random.choice(['Yes', 'No'], N_PATIENTS),
    # ... 25+ more variables
}

# Create realistic correlations
# CNV risk based on clinical factors
cnv_risk = 0.25  # Base rate
cnv_risk += (data['foveal_involvement'] == 'Yes') * 0.25
cnv_risk += data['rupture_length_mm'] * 0.03
# ... sophisticated risk modeling

df = pd.DataFrame(data)
df.to_csv('choroidal_rupture_data.csv')"""

ax.text(0.05, 0.95, code_text, transform=ax.transAxes,
        fontfamily='monospace', fontsize=10,
        verticalalignment='top', color='#D4D4D4')

# Title bar
title_bg = Rectangle((0, 0.96), 1, 0.04, transform=ax.transAxes,
                     facecolor='#2D2D30', zorder=1)
ax.add_patch(title_bg)
ax.text(0.02, 0.98, '📄 generate_synthetic_data.py', transform=ax.transAxes,
        fontsize=11, verticalalignment='center', color='white', fontweight='bold')

plt.savefig('code_example.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: code_example.png")
plt.close()

# ============================================================================
# 4. DEMO PHASES VISUAL
# ============================================================================
print("4. Creating demo phases timeline...")

fig, ax = plt.subplots(figsize=(14, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')

phases = [
    {'name': 'Data\nGeneration', 'time': '5 min', 'icon': '📊', 'color': '#3498DB'},
    {'name': 'Exploratory\nAnalysis', 'time': '4 min', 'icon': '📈', 'color': '#9B59B6'},
    {'name': 'Predictive\nModeling', 'time': '4 min', 'icon': '🤖', 'color': '#E74C3C'},
    {'name': 'Visualization', 'time': '2 min', 'icon': '📉', 'color': '#F39C12'},
    {'name': 'Web App\nDevelopment', 'time': '3 min', 'icon': '🌐', 'color': '#2ECC71'}
]

x_pos = 0.5
for i, phase in enumerate(phases):
    # Box
    box = FancyBboxPatch((x_pos, 1.5), 1.6, 2, boxstyle="round,pad=0.15",
                         edgecolor=phase['color'], facecolor=phase['color'],
                         linewidth=3, alpha=0.9)
    ax.add_patch(box)

    # Icon
    ax.text(x_pos + 0.8, 3, phase['icon'], ha='center', va='center',
            fontsize=32)

    # Phase name
    ax.text(x_pos + 0.8, 2.2, phase['name'], ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')

    # Time
    ax.text(x_pos + 0.8, 1.7, phase['time'], ha='center', va='center',
            fontsize=9, color='white', style='italic')

    # Arrow (except last)
    if i < len(phases) - 1:
        ax.arrow(x_pos + 1.7, 2.5, 0.2, 0, head_width=0.3, head_length=0.08,
                fc='#34495E', ec='#34495E', linewidth=2)

    x_pos += 1.9

# Title
ax.text(5, 4.3, 'Live Demo: 5-Phase Pipeline (~18 minutes)', ha='center',
        fontsize=14, fontweight='bold')

# Subtitle
ax.text(5, 0.7, 'Watch the agent work autonomously through each phase',
        ha='center', fontsize=11, style='italic', color='#7F8C8D')

plt.tight_layout()
plt.savefig('demo_phases.png', dpi=300, bbox_inches='tight', facecolor='white')
print("   ✓ Saved: demo_phases.png")
plt.close()

# ============================================================================
# 5. PROMPT FRAMEWORK VISUAL
# ============================================================================
print("5. Creating 4-C framework diagram...")

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, 'The 4-C Prompt Engineering Framework', ha='center',
        fontsize=16, fontweight='bold')

# Four quadrants
quadrants = [
    {'name': 'CONTEXT', 'pos': (1, 6), 'color': '#3498DB',
     'text': 'Set the stage\n\n"I\'m studying choroidal\nrupture outcomes"'},
    {'name': 'CLEAR GOAL', 'pos': (6, 6), 'color': '#E74C3C',
     'text': 'What you want\n\n"Create a database of\n1000 patients"'},
    {'name': 'CONSTRAINTS', 'pos': (1, 1), 'color': '#F39C12',
     'text': 'Specifications\n\n"Include 25-30 clinically\nrelevant variables"'},
    {'name': 'COLLABORATION', 'pos': (6, 1), 'color': '#2ECC71',
     'text': 'Iterate\n\n"Show me the structure\nfirst, then adjust"'}
]

for q in quadrants:
    # Box
    box = FancyBboxPatch(q['pos'], 3.5, 3.5, boxstyle="round,pad=0.2",
                         edgecolor=q['color'], facecolor=q['color'],
                         linewidth=4, alpha=0.85)
    ax.add_patch(box)

    # Title
    ax.text(q['pos'][0] + 1.75, q['pos'][1] + 3.1, q['name'],
            ha='center', va='center', fontsize=13, fontweight='bold',
            color='white')

    # Content
    ax.text(q['pos'][0] + 1.75, q['pos'][1] + 1.5, q['text'],
            ha='center', va='center', fontsize=10, color='white',
            style='italic')

plt.tight_layout()
plt.savefig('prompt_framework.png', dpi=300, bbox_inches='tight', facecolor='white')
print("   ✓ Saved: prompt_framework.png")
plt.close()

print("\n" + "=" * 70)
print("✓ All supporting visual assets created!")
print("=" * 70)
print("\nCreated:")
print("  • workflow_diagram.png - Agentic workflow")
print("  • database_preview.png - First 5 patients")
print("  • code_example.png - Agent-generated code")
print("  • demo_phases.png - 5-phase timeline")
print("  • prompt_framework.png - 4-C framework")
print("=" * 70)
