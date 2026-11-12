
from pathlib import Path

import numpy as np
import pandas as pd


# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

ANOMALY_THRESHOLD_DAYS = 180

FACTORY_COORDS = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.11914, -96.18115),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.1175, -89.971107),
}

PRODUCT_FACTORY = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory",
}

REQUIRED_COLUMNS = [
    "Row ID",
    "Order ID",
    "Order Date",
    "Ship Date",
    "Ship Mode",
    "Customer ID",
    "Country/Region",
    "City",
    "State/Province",
    "Postal Code",
    "Division",
    "Region",
    "Product ID",
    "Product Name",
    "Sales",
    "Units",
    "Gross Profit",
    "Cost",
]


# --------------------------------------------------
# DATA LOADING AND VALIDATION
# --------------------------------------------------

def load_data(path):
    """
    Load source data and create transparent derived fields.

    Original date values are parsed using day-month-year format.
    No automatic date correction or date shifting is performed.
    """

    path = Path(path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {path}. "
            "Keep the CSV in the project's data folder."
        )

    df = pd.read_csv(
        path,
        dtype={"Postal Code": str}
    )

    # Validate required source columns.
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Dataset is missing required columns: "
            + ", ".join(missing_columns)
        )

    # --------------------------------------------------
    # DATE PROCESSING
    # --------------------------------------------------

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    df["Lead Time Days"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    # --------------------------------------------------
    # FACTORY MAPPING
    # --------------------------------------------------

    df["Factory"] = df["Product Name"].map(
        PRODUCT_FACTORY
    )

    df["Factory Latitude"] = df["Factory"].map(
        lambda factory: (
            FACTORY_COORDS[factory][0]
            if pd.notna(factory)
            else np.nan
        )
    )

    df["Factory Longitude"] = df["Factory"].map(
        lambda factory: (
            FACTORY_COORDS[factory][1]
            if pd.notna(factory)
            else np.nan
        )
    )

    # --------------------------------------------------
    # DATE ANOMALY DETECTION
    # --------------------------------------------------

    df["Date anomaly"] = (
        df["Lead Time Days"].isna()
        | (df["Lead Time Days"] < 0)
        | (
            df["Lead Time Days"]
            > ANOMALY_THRESHOLD_DAYS
        )
    )

    # --------------------------------------------------
    # ROUTE GENERATION
    # --------------------------------------------------

    customer_state = (
        df["State/Province"]
        .fillna("Unknown state")
        .astype(str)
        .str.strip()
    )

    factory_name = (
        df["Factory"]
        .fillna("Unmapped factory")
        .astype(str)
    )

    df["Route"] = (
        factory_name + " to " + customer_state
    )

    # --------------------------------------------------
    # DATA QUALITY AUDIT
    # --------------------------------------------------

    lead_times = df["Lead Time Days"]

    audit = {
        "rows": int(len(df)),

        "source_columns": int(len(REQUIRED_COLUMNS)),

        "source_missing_cells": int(
            df[REQUIRED_COLUMNS].isna().sum().sum()
        ),

        "duplicate_full_rows": int(
            df[REQUIRED_COLUMNS].duplicated().sum()
        ),

        "duplicate_row_ids": int(
            df["Row ID"].duplicated().sum()
        ),

        "duplicate_order_ids": int(
            df["Order ID"].duplicated().sum()
        ),

        "distinct_products": int(
            df["Product Name"].nunique()
        ),

        "invalid_order_dates": int(
            df["Order Date"].isna().sum()
        ),

        "invalid_ship_dates": int(
            df["Ship Date"].isna().sum()
        ),

        "negative_lead_times": int(
            (lead_times < 0).sum()
        ),

        "over_180_day_lead_times": int(
            (lead_times > ANOMALY_THRESHOLD_DAYS).sum()
        ),

        "date_anomaly_rows": int(
            df["Date anomaly"].sum()
        ),

        "unmapped_products": int(
            df["Factory"].isna().sum()
        ),

        "lead_time_min": (
            int(lead_times.min())
            if lead_times.notna().any()
            else None
        ),

        "lead_time_median": (
            float(lead_times.median())
            if lead_times.notna().any()
            else None
        ),

        "lead_time_max": (
            int(lead_times.max())
            if lead_times.notna().any()
            else None
        ),
    }

    return df, audit
