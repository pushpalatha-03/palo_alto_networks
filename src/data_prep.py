
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

ORDINAL_COLS = [
    "EnvironmentSatisfaction", "JobInvolvement", "JobSatisfaction",
    "RelationshipSatisfaction", "WorkLifeBalance", "Education",
    "PerformanceRating", "StockOptionLevel",
]


def load_data(path: str) -> pd.DataFrame:
    """Load the raw employee dataset from CSV."""
    return pd.read_csv(path)


def validate_ordinals(df: pd.DataFrame, cols=ORDINAL_COLS, valid_range=(1, 5)) -> pd.DataFrame:
    """Flag any ordinal values that fall outside the expected 1-5 range."""
    for c in cols:
        if c not in df.columns:
            continue
        bad = df[~df[c].between(*valid_range) & df[c].notna()]
        if len(bad):
            print(f"Warning: {c} has {len(bad)} out-of-range values")
    return df


def handle_missing_satisfaction(df: pd.DataFrame, cols=ORDINAL_COLS) -> pd.DataFrame:
    """Median-impute missing ordinal/satisfaction values (safe default for Likert data)."""
    df = df.copy()
    for c in cols:
        if c in df.columns and df[c].isna().any():
            df[c] = df[c].fillna(df[c].median())
    return df


def normalize_scores(df: pd.DataFrame, cols) -> pd.DataFrame:
    """Add 0-1 min-max normalized versions of the given columns as `{col}_norm`."""
    df = df.copy()
    scaler = MinMaxScaler()
    df[[f"{c}_norm" for c in cols]] = scaler.fit_transform(df[cols])
    return df


def clean_pipeline(path: str) -> pd.DataFrame:
    """Convenience wrapper: load, validate, and impute in one call."""
    df = load_data(path)
    df = validate_ordinals(df)
    df = handle_missing_satisfaction(df)
    return df