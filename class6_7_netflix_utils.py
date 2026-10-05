import logging
import re

import pandas as pd

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    logger.debug(f"DataFrame shape: {df.shape}")

    print("Shape:", df.shape)
    print("\nFirst five rows:")
    print(df.head())
    print("\nColumns:", list(df.columns))
    print("\nData types:")
    print(df.dtypes)


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    logger.debug(
        f"Duplicate removal: {before} rows before, {after} rows after"
    )

    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    before = len(df)
    df = df.dropna()
    after = len(df)

    logger.debug(
        f"Missing-value removal: {before} rows before, {after} rows after"
    )

    return df


def clean_text(value):
    """Clean a text value."""
    if pd.isna(value):
        return value

    value = str(value).strip().lower()
    value = re.sub(r"\s+", " ", value)

    return value


def remove_iqr_outliers(df, column, threshold=1.5):
    """Remove rows containing IQR outliers in a numeric column."""
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' must be numeric")

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr

    before = len(df)

    df = df[
        (df[column] >= lower_bound)
        & (df[column] <= upper_bound)
    ]

    logger.debug(
        f"IQR outlier removal for {column}: "
        f"{before} rows before, {len(df)} rows after"
    )

    return df