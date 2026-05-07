# NYC Food Safety Dashboard

An interactive Dash dashboard built from New York City restaurant inspection data to explore food safety outcomes across boroughs, cuisines, inspection trends, and restaurant-level map views.

## Driving Question

How do food safety outcomes vary across restaurants, boroughs, cuisines, and inspection patterns in New York City, and how can those patterns help users make safer dining decisions?

## Project Summary

This project began as a milestone-based notebook analysis and evolved into an interactive Dash application. The final dashboard combines:

- data wrangling and cleaning
- feature engineering
- comparative charting
- map-based restaurant exploration
- click-based inspection detail review

The intended audience includes:

- students
- diners
- tourists
- classmates and instructors interested in interactive data analysis

## Main Files

- `app.py`
  Main Dash application. Handles layout, charts, filters, map interaction, and callbacks.

- `data_utils.py`
  Loads the dataset, cleans the data, engineers features, and provides filter-ready dataframes for the app.

- `assets/styles.css`
  Controls the visual design of the dashboard.

- `requirements.txt`
  Lists the Python packages needed to run the project.

- `nyc_food_safety_milestone_3.ipynb`
  Notebook used for milestone analysis, chart development, and exploratory work.

- `CLASS_PRESENTATION_GUIDE.txt`
  Class-facing script, rubric answers, and likely Q&A.

- `GITHUB_SUBMISSION_README.txt`
  Milestone-by-milestone project narrative for submission support.

## How To Run The Dashboard Locally

1. Open Terminal
2. Move into the project folder:

```bash
cd /path/to/your/repo
```

3. Install dependencies if needed:

```bash
pip3 install -r requirements.txt
```

4. Start the Dash app:

```bash
python3 app.py
```

5. Open the browser and go to:

```text
http://127.0.0.1:8050
```

## Data Setup

The app checks for the dataset in the following order:

1. `data/nyc_inspection_data.csv.gz`
2. `nyc_inspection_data.csv.gz` in the project root
3. `nyc_inspection_data.csv` in the project root
4. `data/nyc_inspection_data.csv`
5. the original local Desktop path used during development

For a clean GitHub workflow, the best option is to place the CSV in:

- `data/nyc_inspection_data.csv.gz`

The compressed `.csv.gz` version is preferred for GitHub because it keeps the full dataset available while staying within repository file size limits.

## Dashboard Features

- KPI summary cards
- borough comparison chart
- inspection trend over time
- cuisine risk landscape chart
- violation category summary
- interactive NYC restaurant map
- map filters by borough, cuisine, and restaurant name
- click-based restaurant inspection detail card
- safer-picks table

## Data Wrangling and Feature Engineering

Main wrangling steps:

- standardized and renamed columns
- converted dates and numeric values
- cleaned missing and invalid text values
- removed unusable records
- removed duplicate rows
- handled invalid placeholder values such as borough value `0`

Main engineered features:

- `risk_level` from inspection score
- `year` and `year_month` from inspection date
- `violation_category` from raw violation descriptions
- latest-inspection restaurant snapshot
- cleaned display labels for the map and dropdowns

## Limitations

- The dataset is inspection-based, so one restaurant can appear multiple times historically.
- Some source fields were missing, invalid, or not reported.
- Violation categories are simplified groups, not full natural-language analysis.
- The map only shows records with usable NYC coordinates.

## Future Improvements

- deeper borough-over-time comparison
- more advanced text analysis of violations
- dynamic filtering improvements
- public deployment after final local testing

## Submission Notes

If this repository is being used for a class final project submission, the most important files to highlight are:

- `app.py`
- `data_utils.py`
- `assets/styles.css`
- `requirements.txt`
- `nyc_food_safety_milestone_3.ipynb`
- `README.md`

These show the complete flow from analysis to interactive dashboard delivery.
