from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# Chunk 1: Candidate file paths for the source dataset
# Why this exists:
# The app needs a reliable way to find the inspection CSV.
# This list allows the project to check a few expected locations.
# ============================================================
DATA_PATH_OPTIONS = [
    Path("/Users/shahbazshaikh/Desktop/indata_sp26/nyc_food_safety:/nyc_inspection_data.csv"),
    Path(__file__).resolve().parent / "nyc_inspection_data.csv",
    Path(__file__).resolve().parent / "data" / "nyc_inspection_data.csv",
]


# ============================================================
# Chunk 2: Data container used by the dashboard
# Why this exists:
# This dataclass groups the cleaned datasets and filter options
# into one object that can be passed to the Dash app cleanly.
# ============================================================
@dataclass
class DataBundle:
    usable: pd.DataFrame
    latest: pd.DataFrame
    map_df: pd.DataFrame
    grade_options: list[str]
    risk_options: list[str]
    borough_options: list[str]
    cuisine_options: list[str]
    restaurant_options: list[str]


# ============================================================
# Chunk 3: Locate the dataset on disk
# Why this exists:
# The app should fail clearly if the CSV is missing, instead of
# producing confusing errors later in the workflow.
# ============================================================
def locate_data_path() -> Path:
    for path in DATA_PATH_OPTIONS:
        if path.exists():
            return path
    searched = "\n".join(str(path) for path in DATA_PATH_OPTIONS)
    raise FileNotFoundError(
        "Could not find `nyc_inspection_data.csv`. Checked these locations:\n"
        f"{searched}"
    )


# ============================================================
# Chunk 4: Build a human-readable risk bucket from score
# Why this exists:
# Raw inspection score is numeric, but a dashboard benefits from
# a simpler category such as Low, Medium, or High risk.
# ============================================================
def risk_bucket(score: float) -> str | float:
    if pd.isna(score):
        return np.nan
    if score <= 13:
        return "Low"
    if score <= 27:
        return "Medium"
    return "High"


# ============================================================
# Chunk 5: Simplify long violation descriptions
# Why this exists:
# Raw violation text is too detailed and repetitive for quick
# dashboard reading, so this groups it into broader categories.
# ============================================================
def simplify_violation(desc: str) -> str:
    desc = str(desc).lower()

    if "hand washing" in desc or "handwashing" in desc or "hand wash" in desc:
        return "Hand Washing Issues"
    if "sanitiz" in desc or "dishwashing" in desc or "ware washing" in desc:
        return "Cleaning and Sanitizing"
    if "temperature" in desc or "cold holding" in desc or "hot holding" in desc:
        return "Food Temperature Problems"
    if (
        "evidence of mice" in desc
        or "live roaches" in desc
        or "vermin" in desc
        or "pest" in desc
    ):
        return "Pest / Vermin Issues"
    if "sewage" in desc or "plumbing" in desc or "drain" in desc:
        return "Plumbing / Sewage Problems"
    if "food contact surface" in desc or "equipment" in desc or "utensil" in desc:
        return "Equipment / Surface Issues"
    if "toilet" in desc or "facility" in desc or "washing facility" in desc:
        return "Facility Maintenance Issues"
    if "food worker" in desc or "personal cleanliness" in desc:
        return "Worker Hygiene Issues"
    if "storage" in desc or "adulterated" in desc or "contaminated" in desc:
        return "Food Storage / Contamination"
    if "label" in desc or "posting" in desc or "permit" in desc:
        return "Labeling / Posting / Permit"
    return "Other Violations"


# ============================================================
# Chunk 6: Main data-loading and cleaning pipeline
# Why this exists:
# This function loads the raw CSV, standardizes it, engineers
# dashboard-ready fields, and prepares filter options.
# ============================================================
def load_data_bundle() -> DataBundle:
    data_path = locate_data_path()
    raw = pd.read_csv(data_path)

    # ------------------------------------------------------------
    # Chunk 6A: Standardize raw columns and basic field types
    # Purpose:
    # Make the source dataset consistent before any analysis.
    # ------------------------------------------------------------
    df = raw.copy()
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    )
    df = df.rename(columns={"boro": "borough", "zip": "zipcode", "bldg": "building"})

    for date_col in ["inspection_date", "grade_date", "record_date"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    if "score" in df.columns:
        df["score"] = pd.to_numeric(df["score"], errors="coerce")

    if "zipcode" in df.columns:
        df["zipcode"] = df["zipcode"].astype(str).str.extract(r"(\d{5})", expand=False)

    # ------------------------------------------------------------
    # Chunk 6B: Clean text fields and normalize placeholder values
    # Purpose:
    # Convert empty strings, string NaNs, and placeholder-style
    # values such as "0" into missing values where appropriate.
    # ------------------------------------------------------------
    text_cols = [
        "dba",
        "borough",
        "cuisine_description",
        "inspection_type",
        "action",
        "grade",
        "critical_flag",
        "violation_description",
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .replace({"": np.nan, "nan": np.nan, "NaN": np.nan, "0": np.nan})
            )

    # ------------------------------------------------------------
    # Chunk 6C: Keep only usable inspection rows
    # Purpose:
    # The dashboard needs valid inspection records, so rows
    # missing key inspection fields are removed.
    # ------------------------------------------------------------
    usable = df.dropna(subset=["inspection_date", "inspection_type"]).copy()
    usable = usable.drop_duplicates().copy()

    # ------------------------------------------------------------
    # Chunk 6D: Fill missing labels and engineer dashboard fields
    # Purpose:
    # Create analysis-ready columns such as year, year-month,
    # risk level, and simplified violation category.
    # ------------------------------------------------------------
    usable["borough"] = usable["borough"].replace({"0": np.nan}).fillna("Not Reported")
    usable["cuisine_description"] = usable["cuisine_description"].fillna("Not Reported")
    usable["dba"] = usable["dba"].fillna("Name Not Reported")
    usable["year"] = usable["inspection_date"].dt.year
    usable["year_month"] = usable["inspection_date"].dt.to_period("M").astype(str)
    usable["risk_level"] = usable["score"].apply(risk_bucket)
    usable["has_critical_violation"] = (
        usable["critical_flag"].fillna("").str.lower().eq("critical")
    )
    usable["violation_category"] = usable["violation_description"].apply(simplify_violation)

    # ------------------------------------------------------------
    # Chunk 6E: Create a restaurant-level latest inspection view
    # Purpose:
    # Some charts need one current snapshot per restaurant rather
    # than every inspection row in the historical dataset.
    # ------------------------------------------------------------
    latest = (
        usable.sort_values(["camis", "inspection_date"], ascending=[True, False])
        .drop_duplicates(subset=["camis"], keep="first")
        .copy()
    )

    # ------------------------------------------------------------
    # Chunk 6F: Prepare map-friendly display fields
    # Purpose:
    # Build cleaner labels and filter columns for the map and
    # interactive restaurant lookup.
    # ------------------------------------------------------------
    latest["latitude"] = pd.to_numeric(latest["latitude"], errors="coerce")
    latest["longitude"] = pd.to_numeric(latest["longitude"], errors="coerce")
    latest["restaurant_name"] = latest["dba"].fillna("Name Not Reported")
    latest["cuisine_clean"] = latest["cuisine_description"].fillna("Not Reported").str.title()
    latest["borough_clean"] = latest["borough"].fillna("Not Reported")
    latest["inspection_day"] = latest["inspection_date"].dt.strftime("%b %d, %Y")
    latest["violation_category"] = latest["violation_category"].fillna("Other Violations")
    latest["violation_description"] = latest["violation_description"].fillna("No detailed violation description available.")

    # ------------------------------------------------------------
    # Chunk 6G: Keep only valid NYC coordinates for map use
    # Purpose:
    # The map should only render restaurants with coordinates that
    # fall inside a valid NYC geographic range.
    # ------------------------------------------------------------
    map_df = latest[
        latest["latitude"].between(40.45, 40.95)
        & latest["longitude"].between(-74.30, -73.65)
    ].copy()

    # ------------------------------------------------------------
    # Chunk 6H: Package cleaned data and dropdown options
    # Purpose:
    # Return one structured object containing both the prepared
    # dataframes and the dropdown values used by the app.
    # ------------------------------------------------------------
    return DataBundle(
        usable=usable,
        latest=latest,
        map_df=map_df,
        grade_options=["All Grades"] + sorted(latest["grade"].dropna().astype(str).unique().tolist()),
        risk_options=["All Risk Levels"] + sorted(latest["risk_level"].dropna().astype(str).unique().tolist()),
        borough_options=["All Boroughs"]
        + sorted(latest["borough_clean"].dropna().astype(str).unique().tolist()),
        cuisine_options=["All Restaurant Types"]
        + sorted(latest["cuisine_clean"].dropna().astype(str).unique().tolist()),
        restaurant_options=["All Restaurants"]
        + sorted(latest["restaurant_name"].dropna().astype(str).unique().tolist()),
    )


# ============================================================
# Chunk 7: Apply dashboard filters to the prepared data
# Why this exists:
# Dash callbacks need a reusable way to filter both the full
# inspection dataset and the latest restaurant snapshot.
# ============================================================
def apply_filters(
    usable: pd.DataFrame,
    latest: pd.DataFrame,
    borough: str,
    cuisine: str,
    grade: str,
    risk_level: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    filtered_usable = usable.copy()
    filtered_latest = latest.copy()

    # ------------------------------------------------------------
    # Chunk 7A: Borough filter
    # ------------------------------------------------------------
    if borough != "All Boroughs":
        filtered_usable = filtered_usable[filtered_usable["borough"] == borough]
        filtered_latest = filtered_latest[filtered_latest["borough_clean"] == borough]

    # ------------------------------------------------------------
    # Chunk 7B: Cuisine filter
    # ------------------------------------------------------------
    if cuisine != "All Restaurant Types":
        filtered_usable = filtered_usable[
            filtered_usable["cuisine_description"].str.title() == cuisine
        ]
        filtered_latest = filtered_latest[filtered_latest["cuisine_clean"] == cuisine]

    # ------------------------------------------------------------
    # Chunk 7C: Grade filter
    # ------------------------------------------------------------
    if grade != "All Grades":
        filtered_usable = filtered_usable[filtered_usable["grade"] == grade]
        filtered_latest = filtered_latest[filtered_latest["grade"] == grade]

    # ------------------------------------------------------------
    # Chunk 7D: Risk-level filter
    # ------------------------------------------------------------
    if risk_level != "All Risk Levels":
        filtered_usable = filtered_usable[filtered_usable["risk_level"] == risk_level]
        filtered_latest = filtered_latest[filtered_latest["risk_level"] == risk_level]

    return filtered_usable, filtered_latest
