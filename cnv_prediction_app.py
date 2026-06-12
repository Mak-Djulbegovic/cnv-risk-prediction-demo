"""
CNV Risk Prediction - live clinical decision tool
=================================================
Streamlit UI on top of cnv_core.py (pure, testable logic).

Features
  - One-click clinical preset cases
  - LIVE risk gauge (recomputes on every input change, no button)
  - Individualized CNV-free survival curve (Cox model) + median time marker
  - Honest per-patient explanation (ceteris-paribus vs a typical patient)
  - What-if counterfactuals ("spare the fovea", "halve the rupture")
  - Cohort context: where this patient sits among 1000 cases
  - Phone-share panel (LAN URL + QR) so the audience can open it live

SYNTHETIC DATA - educational demonstration only. NOT for clinical use.
"""

import io
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import cnv_core as core

# ---------------------------------------------------------------------------
# Palette (matches the slide deck)
# ---------------------------------------------------------------------------
NAVY = "#16365C"
TEAL = "#2C7A7B"
CRIMSON = "#C0392B"
AMBER = "#B9770E"
GREEN = "#2E8B57"
INK = "#212529"
GRID = "#E3E7EB"
MUTE = "#5A6570"

st.set_page_config(page_title="CNV Risk - live tool", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown(
    f"""
    <style>
      .block-container {{ padding-top: 1.6rem; max-width: 1280px; }}
      h1, h2, h3 {{ color: {NAVY}; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
      .accent-rule {{ height: 4px; width: 64px; background: {TEAL};
                      border-radius: 2px; margin: 2px 0 14px 0; }}
      .synthetic {{ background: #FBEEE9; border-left: 5px solid {CRIMSON};
                    color: {CRIMSON}; padding: 9px 16px; border-radius: 4px;
                    font-weight: 600; font-size: 0.92rem; margin-bottom: 8px; }}
      .metric-card {{ border: 1px solid {GRID}; border-radius: 10px;
                      padding: 14px 18px; background: #FBFCFD; }}
      .stCaption, .small {{ color: {MUTE}; }}
      div[data-testid="stSidebarHeader"] {{ padding-bottom: 0; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def section(title):
    """Consistent section header: navy title + short teal accent rule."""
    st.markdown(f"#### {title}")
    st.markdown('<div class="accent-rule"></div>', unsafe_allow_html=True)


@st.cache_resource
def _load():
    rf, scaler, features, cox, cohort = core.load_artifacts()
    ref = core.cohort_reference(cohort)
    dist = core.cohort_risk_distribution(rf, scaler, features, cohort)
    km = {
        True: core.cohort_km(cohort, foveal=True),
        False: core.cohort_km(cohort, foveal=False),
    }
    return rf, scaler, features, cox, cohort, ref, dist, km


try:
    rf, scaler, features, cox, cohort, REFERENCE, DIST, KM = _load()
except Exception as exc:  # pragma: no cover - UI guard
    st.error(f"Could not load model artifacts: {exc}")
    st.stop()


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("# CNV risk after traumatic choroidal rupture")
st.markdown('<div class="accent-rule"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="synthetic">SYNTHETIC DATA &middot; educational demonstration only '
    '&middot; NOT for clinical use</div>',
    unsafe_allow_html=True,
)
st.caption(
    "Random forest risk + Cox individualized survival, trained on 1000 synthetic "
    "rupture cases. Every control updates the prediction live."
)


# ---------------------------------------------------------------------------
# Preset handling (writes default widget values via session_state)
# ---------------------------------------------------------------------------
def apply_preset(name):
    d = core.PRESETS[name]
    st.session_state.update({
        "age": d["age"], "sex": d["sex"],
        "rupture_length_mm": float(d["rupture_length_mm"]),
        "distance_from_fovea_um": int(d["distance_from_fovea_um"]),
        "foveal_involvement": bool(d["foveal_involvement"]),
        "choroidal_thickness_um": int(d["choroidal_thickness_um"]),
        "subretinal_hemorrhage": bool(d["subretinal_hemorrhage"]),
        "baseline_cst_um": int(d["baseline_cst_um"]),
        "outer_retinal_disruption_score": int(d["outer_retinal_disruption_score"]),
        "rpe_disruption": bool(d["rpe_disruption"]),
        "ez_integrity_percent": int(d["ez_integrity_percent"]),
        "subretinal_fluid": bool(d["subretinal_fluid"]),
        "intraretinal_cysts": bool(d["intraretinal_cysts"]),
        "baseline_va_logmar": float(d["baseline_va_logmar"]),
    })


# Seed defaults once from the intermediate preset
if "age" not in st.session_state:
    apply_preset("Intermediate - juxtafoveal")

st.sidebar.markdown("### Clinical preset cases")
for name in core.PRESETS:
    st.sidebar.button(name, use_container_width=True,
                      on_click=apply_preset, args=(name,))

st.sidebar.markdown("---")
st.sidebar.markdown("### Patient parameters")

age = st.sidebar.slider("Age (years)", 10, 85, key="age")
sex = st.sidebar.selectbox("Sex", ["Male", "Female"], key="sex")

st.sidebar.markdown("**Rupture**")
rupture_length_mm = st.sidebar.slider("Rupture length (mm)", 0.5, 12.0, step=0.1,
                                      key="rupture_length_mm")
distance_from_fovea_um = st.sidebar.slider("Distance from fovea (\u00b5m)", 0, 5000,
                                           step=50, key="distance_from_fovea_um")
foveal_involvement = st.sidebar.checkbox("Foveal involvement", key="foveal_involvement")
choroidal_thickness_um = st.sidebar.slider("Choroidal thickness (\u00b5m)", 150, 450,
                                           step=10, key="choroidal_thickness_um")
subretinal_hemorrhage = st.sidebar.checkbox("Subretinal hemorrhage",
                                            key="subretinal_hemorrhage")

st.sidebar.markdown("**OCT**")
baseline_cst_um = st.sidebar.slider("Central subfield thickness (\u00b5m)", 180, 600,
                                    step=10, key="baseline_cst_um")
outer_retinal_disruption_score = st.sidebar.select_slider(
    "Outer retinal disruption", options=[0, 1, 2, 3],
    key="outer_retinal_disruption_score")
rpe_disruption = st.sidebar.checkbox("RPE disruption", key="rpe_disruption")
ez_integrity_percent = st.sidebar.slider("EZ integrity (%)", 0, 100, step=5,
                                         key="ez_integrity_percent")
subretinal_fluid = st.sidebar.checkbox("Subretinal fluid", key="subretinal_fluid")
intraretinal_cysts = st.sidebar.checkbox("Intraretinal cysts", key="intraretinal_cysts")

st.sidebar.markdown("**Vision**")
baseline_va_logmar = st.sidebar.slider("Baseline VA (logMAR)", 0.0, 2.0, step=0.1,
                                       key="baseline_va_logmar")
st.sidebar.caption(f"\u2248 Snellen 20/{20 * 10 ** baseline_va_logmar:.0f}")


# ---------------------------------------------------------------------------
# Build the live feature row from current widget state
# ---------------------------------------------------------------------------
raw = dict(
    age=age, sex=sex, rupture_length_mm=rupture_length_mm,
    distance_from_fovea_um=distance_from_fovea_um,
    foveal_involvement=foveal_involvement,
    choroidal_thickness_um=choroidal_thickness_um,
    subretinal_hemorrhage=subretinal_hemorrhage, baseline_cst_um=baseline_cst_um,
    outer_retinal_disruption_score=outer_retinal_disruption_score,
    rpe_disruption=rpe_disruption, ez_integrity_percent=ez_integrity_percent,
    subretinal_fluid=subretinal_fluid, intraretinal_cysts=intraretinal_cysts,
    baseline_va_logmar=baseline_va_logmar,
)
row = core.inputs_to_row(raw)

risk = core.predict_risk(rf, scaler, features, row)
band, band_color = core.risk_band(risk)
times, surv = core.survival_curve(cox, row)
med_t = core.median_time_to_cnv(times, surv)
contrib, _ = core.local_contributions(rf, scaler, features, row, REFERENCE)
pct = core.percentile_of(risk, DIST)
km_times, km_surv, km_n = KM[bool(foveal_involvement)]


# ---------------------------------------------------------------------------
# Row 1: gauge + headline metrics
# ---------------------------------------------------------------------------
g_col, m_col = st.columns([1.15, 1])

with g_col:
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk * 100,
        number={"suffix": "%", "font": {"size": 46, "color": band_color}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": MUTE},
            "bar": {"color": band_color, "thickness": 0.28},
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "#E7F1EC"},
                {"range": [40, 70], "color": "#FBF1DF"},
                {"range": [70, 100], "color": "#FBE6E2"},
            ],
            "threshold": {"line": {"color": INK, "width": 3},
                          "thickness": 0.78, "value": risk * 100},
        },
    ))
    gauge.update_layout(height=260, margin=dict(l=20, r=20, t=10, b=0),
                        paper_bgcolor="white")
    st.plotly_chart(gauge, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        f"<div style='text-align:center;font-size:1.25rem;font-weight:700;"
        f"color:{band_color};margin-top:-12px'>{band} risk of CNV development</div>",
        unsafe_allow_html=True,
    )

with m_col:
    section("At a glance")
    a, b = st.columns(2)
    a.metric("CNV probability", f"{risk * 100:.0f}%",
             help="Random forest probability of CNV development.")
    b.metric("Cohort percentile", f"{pct:.0f}th",
             help="Rank vs 1000 synthetic cases.")
    c, d = st.columns(2)
    c.metric("Median time to CNV",
             f"{med_t:.0f} mo" if med_t is not None else ">36 mo",
             help="First month CNV-free survival falls to 50%.")
    d.metric("36-mo CNV-free", f"{surv[-1] * 100:.0f}%",
             help="Cox-predicted survival at 3 years.")
    st.caption(
        "Percentile is this patient's rank among 1000 synthetic cases; "
        "median time is when CNV-free survival falls to 50%."
    )


# ---------------------------------------------------------------------------
# Row 2: survival curve + honest contributions
# ---------------------------------------------------------------------------
s_col, e_col = st.columns([1, 1])

with s_col:
    section("Individualized vs population survival")
    grp = "foveal involvement" if foveal_involvement else "no foveal involvement"
    fig = go.Figure()
    # population baseline (Kaplan-Meier, matching foveal subgroup)
    fig.add_trace(go.Scatter(
        x=km_times, y=km_surv * 100, mode="lines",
        line=dict(color=MUTE, width=2, dash="dash"),
        name=f"Typical eye \u2014 {grp} (n={km_n})"))
    # this patient (Cox)
    fig.add_trace(go.Scatter(
        x=times, y=surv * 100, mode="lines", line=dict(color=NAVY, width=3.5),
        fill="tonexty", fillcolor="rgba(22,54,92,0.06)",
        name="This patient (Cox)"))
    fig.add_hline(y=50, line=dict(color=MUTE, width=1, dash="dot"))
    if med_t is not None:
        fig.add_vline(x=med_t, line=dict(color=CRIMSON, width=2, dash="dash"))
        fig.add_annotation(x=med_t, y=8, text=f"median {med_t:.0f} mo",
                           showarrow=False, font=dict(color=CRIMSON, size=13),
                           xanchor="left", xshift=6)
    fig.update_layout(
        height=320, margin=dict(l=10, r=10, t=6, b=10), paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0,
                    font=dict(size=12)),
        xaxis=dict(title="Months since rupture", range=[0, 36], gridcolor=GRID),
        yaxis=dict(title="CNV-free survival (%)", range=[0, 102], gridcolor=GRID),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with e_col:
    section("Why this patient (vs a typical case)")
    movers = [c for c in contrib if abs(c["delta"]) > 1e-9][:7]
    if not movers:
        st.info("This patient matches the typical reference case on every driver.")
    else:
        labels = [c["label"] for c in movers][::-1]
        deltas = [c["delta"] * 100 for c in movers][::-1]
        colors = [CRIMSON if x > 0 else TEAL for x in deltas]
        bar = go.Figure(go.Bar(
            x=deltas, y=labels, orientation="h",
            marker=dict(color=colors),
            text=[f"{x:+.0f}" for x in deltas], textposition="outside",
            cliponaxis=False))
        bar.update_layout(
            height=320, margin=dict(l=10, r=30, t=6, b=10), paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(title="Risk shift vs typical patient (percentage points)",
                       gridcolor=GRID, zerolinecolor=MUTE),
            yaxis=dict(automargin=True))
        st.plotly_chart(bar, use_container_width=True,
                        config={"displayModeBar": False})
        st.caption("Red pushes this patient's risk up, teal pulls it down "
                   "\u2014 each factor swapped to the cohort-median value.")


# ---------------------------------------------------------------------------
# Row 3: cohort context
# ---------------------------------------------------------------------------
section("Where this patient sits among 1000 cases")
hist = go.Figure()
hist.add_trace(go.Histogram(
    x=DIST * 100, nbinsx=30, marker=dict(color=GRID, line=dict(width=0)),
    name="Cohort"))
hist.add_vline(x=risk * 100, line=dict(color=band_color, width=3))
hist.add_annotation(x=risk * 100, y=1, yref="paper", yanchor="bottom",
                    text=f"this patient ({pct:.0f}th pct)", showarrow=False,
                    font=dict(color=band_color, size=13))
hist.update_layout(
    height=300, margin=dict(l=10, r=10, t=24, b=10), paper_bgcolor="white",
    plot_bgcolor="white", showlegend=False, bargap=0.05,
    xaxis=dict(title="Predicted CNV risk (%)", range=[0, 100], gridcolor=GRID),
    yaxis=dict(title="Patients", gridcolor=GRID))
st.plotly_chart(hist, use_container_width=True,
                config={"displayModeBar": False})


# ---------------------------------------------------------------------------
# Sidebar: phone share (LAN URL + QR)
# ---------------------------------------------------------------------------
st.sidebar.markdown("---")
with st.sidebar.expander("Share to phones (same wifi)"):
    ip = core.lan_ip()
    url = f"http://{ip}:8501"
    st.write(f"Open on any device on this network:")
    st.code(url, language=None)
    try:
        import qrcode
        img = qrcode.make(url)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=170)
    except Exception:
        st.caption("Install `qrcode` to show a scannable code.")


# ---------------------------------------------------------------------------
# Takeaway report
# ---------------------------------------------------------------------------
st.markdown("---")
report = core.build_report(raw, risk, band, pct, med_t,
                           surv[-1], contrib)
dl_col, _ = st.columns([1, 3])
with dl_col:
    st.download_button(
        "Download assessment (.txt)", data=report,
        file_name="cnv_risk_assessment.txt", mime="text/plain",
        use_container_width=True)


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Random forest (AUC \u2248 0.77) for risk \u00b7 Cox proportional hazards for "
    "timing \u00b7 explanations are model-based ceteris-paribus shifts, not SHAP. "
    "SYNTHETIC DATA \u2014 educational demonstration only, NOT for clinical use."
)
