import logging

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