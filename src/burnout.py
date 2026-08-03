"""
Burnout risk identification and workload/stress scoring for the
PAN Engagement & Burnout project.
"""

import pandas as pd


def burnout_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag burnout risk from three signals: overtime, poor work-life balance,
    and low engagement. Score 0-3 -> bucketed into Low / Medium / High.
    """
    df = df.copy()
    overtime_flag = (df["OverTime"] == "Yes").astype(int)
    low_wlb_flag = (df["WorkLifeBalance"] <= 2).astype(int)
    low_engagement_flag = (df["EngagementIndex"] <= 2).astype(int)

    df["BurnoutRiskScore"] = overtime_flag + low_wlb_flag + low_engagement_flag

    def bucket(score):
        if score >= 2:
            return "High"
        elif score == 1:
            return "Medium"
        return "Low"

    df["BurnoutRiskLevel"] = df["BurnoutRiskScore"].apply(bucket)
    return df


def workload_stress_indicator(df: pd.DataFrame) -> pd.DataFrame:
    """Combine travel frequency and overtime into a single workload stress score."""
    df = df.copy()
    travel_weight = df["BusinessTravel"].map({
        "Non-Travel": 0, "Travel_Rarely": 1, "Travel_Frequently": 2
    }).fillna(0)
    overtime_weight = (df["OverTime"] == "Yes").astype(int) * 2
    df["WorkloadStressIndicator"] = travel_weight + overtime_weight
    return df


def run_burnout_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Convenience wrapper: apply both burnout scoring functions."""
    df = burnout_risk_score(df)
    df = workload_stress_indicator(df)
    return df