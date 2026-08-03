import sys
import os
import pandas as pd
import streamlit as st
import plotly.express as px

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from data_prep import validate_ordinals, handle_missing_satisfaction
from indices import build_engagement_index, satisfaction_stability_score, career_stage_bucket
from burnout import burnout_risk_score, workload_stress_indicator

st.set_page_config(page_title="PAN Engagement & Burnout Diagnostic", layout="wide")
st.title("Employee Engagement, Satisfaction & Burnout Diagnostic")
st.caption("Palo Alto Networks — Preventive HR Analytics")

# ---------------------------------------------------------------
# Data loading + full pipeline
# ---------------------------------------------------------------
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw_employee_data.csv")


def run_full_pipeline(raw: pd.DataFrame) -> pd.DataFrame:
    df = validate_ordinals(raw)
    df = handle_missing_satisfaction(df)
    df = build_engagement_index(df)
    df = satisfaction_stability_score(df)
    df = career_stage_bucket(df)
    df = burnout_risk_score(df)
    df = workload_stress_indicator(df)
    return df


@st.cache_data
def load_data(path):
    raw = pd.read_csv(path)
    return run_full_pipeline(raw)


uploaded = st.sidebar.file_uploader("Upload dataset (optional)", type="csv")
if uploaded is not None:
    df = run_full_pipeline(pd.read_csv(uploaded))
elif os.path.exists(DEFAULT_PATH):
    df = load_data(DEFAULT_PATH)
else:
    st.warning("No dataset found. Upload a CSV in the sidebar to begin.")
    st.stop()

# ---------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------
st.sidebar.header("Filters")

dept_choices = sorted(df["Department"].unique().tolist())
dept = st.sidebar.multiselect("Choose Department(s)", dept_choices, default=[])

if len(dept) == 0:
    st.info("👈 Please choose one or more departments from the sidebar to view the dashboard.")
    st.stop()

role_choices = sorted(df[df["Department"].isin(dept)]["JobRole"].unique().tolist())
role = st.sidebar.multiselect("Choose Job Role(s)", role_choices, default=role_choices)

overtime_only = st.sidebar.checkbox("Overtime employees only")
eng_threshold = st.sidebar.slider("Min Engagement Index", 0, 100, 0)
tenure_range = st.sidebar.slider(
    "Years at Company", 0, int(df["YearsAtCompany"].max()),
    (0, int(df["YearsAtCompany"].max()))
)

f = df[df["Department"].isin(dept) & df["JobRole"].isin(role)]

if overtime_only:
    f = f[f["OverTime"] == "Yes"]
f = f[f["EngagementIndex_100"] >= eng_threshold]
f = f[f["YearsAtCompany"].between(*tenure_range)]

if f.empty:
    st.warning("No employees match the current filters.")
    st.stop()

# ---------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Engagement Health Overview",
    "Burnout Risk Dashboard",
    "Role & Career Stage Analysis",
    "Manager Action Panel",
])

# ---- Tab 1: Engagement Health Overview ----
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Org Engagement Index", f"{f['EngagementIndex_100'].mean():.1f} / 100")
    c2.metric("Avg Work-Life Balance", f"{f['WorkLifeBalance'].mean():.2f} / 4")
    c3.metric("Avg Satisfaction Stability", f"{f['SatisfactionStability'].mean():.2f}")
    c4.metric("Employees in view", len(f))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            px.histogram(f, x="EngagementIndex_100", nbins=20,
                          title="Engagement Score Distribution",
                          color_discrete_sequence=["#2563eb"]),
            use_container_width=True,
        )
    with col2:
        dept_eng = f.groupby("Department")["EngagementIndex_100"].mean().reset_index()
        st.plotly_chart(
            px.bar(dept_eng, x="Department", y="EngagementIndex_100",
                   title="Avg Engagement by Department",
                   color_discrete_sequence=["#10b981"]),
            use_container_width=True,
        )

    sat_cols = ["JobInvolvement", "JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction"]
    sat_avg = f[sat_cols].mean().reset_index()
    sat_avg.columns = ["Dimension", "Avg Score"]
    st.plotly_chart(
        px.bar(sat_avg, x="Dimension", y="Avg Score", title="Satisfaction Dimensions (org avg)",
               range_y=[0, 4], color_discrete_sequence=["#6366f1"]),
        use_container_width=True,
    )

# ---- Tab 2: Burnout Risk Dashboard ----
with tab2:
    c1, c2, c3 = st.columns(3)
    risk_counts = f["BurnoutRiskLevel"].value_counts()
    c1.metric("High Risk", int(risk_counts.get("High", 0)))
    c2.metric("Medium Risk", int(risk_counts.get("Medium", 0)))
    c3.metric("Low Risk", int(risk_counts.get("Low", 0)))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            px.pie(f, names="BurnoutRiskLevel", title="Burnout Risk Segments",
                   color="BurnoutRiskLevel",
                   color_discrete_map={"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"}),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            px.box(f, x="OverTime", y="WorkloadStressIndicator",
                   title="Workload Stress by Overtime Status",
                   color_discrete_sequence=["#f97316"]),
            use_container_width=True,
        )

    attr_by_risk = f.groupby("BurnoutRiskLevel")["Attrition"].mean().reindex(["Low", "Medium", "High"]) * 100
    st.plotly_chart(
        px.bar(attr_by_risk.reset_index(), x="BurnoutRiskLevel", y="Attrition",
               title="Attrition Rate (%) by Burnout Risk Level",
               labels={"Attrition": "Attrition Rate (%)"},
               color_discrete_sequence=["#ef4444"]),
        use_container_width=True,
    )

    st.subheader("High-Risk Employee Segments")
    st.dataframe(
        f[f["BurnoutRiskLevel"] == "High"][
            ["JobRole", "Department", "OverTime", "WorkLifeBalance", "EngagementIndex_100", "BusinessTravel"]
        ].sort_values("EngagementIndex_100")
    )

# ---- Tab 3: Role & Career Stage Analysis ----
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            px.box(f, x="JobLevel", y="EngagementIndex_100", title="Engagement by Job Level",
                   color_discrete_sequence=["#2563eb"]),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            px.scatter(f, x="YearsAtCompany", y="EngagementIndex_100", color="JobRole",
                       title="Tenure vs Engagement"),
            use_container_width=True,
        )

    promo_eng = f.groupby("PromoBucket", observed=True)["EngagementIndex_100"].mean().reset_index()
    st.plotly_chart(
        px.bar(promo_eng, x="PromoBucket", y="EngagementIndex_100",
               title="Engagement by Years Since Last Promotion (stagnation check)",
               color_discrete_sequence=["#8b5cf6"]),
        use_container_width=True,
    )

    role_eng = f.groupby("JobRole")["EngagementIndex_100"].mean().sort_values().reset_index()
    st.plotly_chart(
        px.bar(role_eng, x="EngagementIndex_100", y="JobRole", orientation="h",
               title="Engagement by Job Role", color_discrete_sequence=["#0ea5e9"]),
        use_container_width=True,
    )

# ---- Tab 4: Manager Action Panel ----
with tab4:
    st.subheader("Low-Engagement Alerts")
    alerts = f[f["EngagementIndex_100"] < 40].sort_values("EngagementIndex_100")
    st.write(f"**{len(alerts)}** employees below the 40/100 engagement threshold.")
    st.dataframe(
        alerts[["JobRole", "Department", "EngagementIndex_100", "BurnoutRiskLevel", "OverTime", "WorkLifeBalance"]]
    )
    st.download_button(
        "Export alert list (CSV)",
        alerts.to_csv(index=False),
        "low_engagement_alerts.csv",
    )

    st.subheader("Priority Intervention Areas")
    priority = (
        f[f["BurnoutRiskLevel"] == "High"]
        .groupby("Department")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="High Risk Count")
    )
    st.dataframe(priority)