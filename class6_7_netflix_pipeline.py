import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
    show_overview,
)


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )

    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    data_path = Path(args.input)

    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        logger.error(f"Input file not found: {data_path}")
        sys.exit(1)

    logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns")

    # Save the original DataFrame for comparison
    df_original = df.copy()

    show_overview(df)
    logger.info("Displayed DataFrame overview")

    # Remove duplicate rows
    before = len(df)
    df = remove_duplicates(df)
    logger.info(f"Removed {before - len(df)} duplicate row(s)")

    # Remove rows with missing values
    before = len(df)
    df = drop_missing_rows(df)
    logger.info(f"Dropped {before - len(df)} rows with missing values")

    # Remove runtime outliers using the IQR method
    before = len(df)

    try:
        df = remove_iqr_outliers(
            df,
            "runtime_minutes",
            threshold=1.5
        )
    except ValueError as error:
        logger.error(error)
        sys.exit(1)

    logger.info(
        f"Removed {before - len(df)} runtime outlier row(s)"
    )

    # Clean text columns
    text_columns = ["title", "type", "country"]

    for column in text_columns:
        df[column] = df[column].apply(clean_text)

    logger.info("Cleaned text columns: title, type, country")

    # Final cleaning report
    report = {
        "rows_before": len(df_original),
        "rows_after": len(df),
        "rows_removed": len(df_original) - len(df),
        "columns": list(df.columns),
    }

    logger.info(f"Cleaning report: {report}")


if __name__ == "__main__":
    main()