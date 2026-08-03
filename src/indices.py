"""
Engagement index construction for the PAN Engagement & Burnout project.

Combines JobInvolvement, JobSatisfaction, EnvironmentSatisfaction, and
RelationshipSatisfaction into a single, standardized engagement score.
""" 

import pandas as pd

ENGAGEMENT_COMPONENTS = [
    "JobInvolvement", "JobSatisfaction",
    "EnvironmentSatisfaction", "RelationshipSatisfaction",
]


def build_engagement_index(df: pd.DataFrame) -> pd.DataFrame:
    """Add EngagementIndex (1-4 scale) and EngagementIndex_100 (0-100 scale)."""
    df = df.copy()
    df["EngagementIndex"] = df[ENGAGEMENT_COMPONENTS].mean(axis=1)
    df["EngagementIndex_100"] = (df["EngagementIndex"] - 1) / 3 * 100
    return df


def satisfaction_stability_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add SatisfactionStability: higher when the four satisfaction dimensions
    agree with each other (low std dev), lower when they diverge.
    """
    df = df.copy()
    df["SatisfactionStability"] = 1 / (1 + df[ENGAGEMENT_COMPONENTS].std(axis=1))
    return df


def career_stage_bucket(df: pd.DataFrame) -> pd.DataFrame:
    """Bucket YearsSinceLastPromotion to support stagnation analysis."""
    df = df.copy()
    df["PromoBucket"] = pd.cut(
        df["YearsSinceLastPromotion"], bins=[-1, 0, 2, 5, 100],
        labels=["0", "1-2", "3-5", "6+"]
    )
    return df