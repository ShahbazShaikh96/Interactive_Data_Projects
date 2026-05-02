NYC FOOD SAFETY DASHBOARD
FINAL PROJECT SUBMISSION GUIDE

This file is written as a submission-ready explanation of the project
from Milestone 1 through Milestone 3. It focuses on what changed,
why those changes were made, and how the final dashboard reflects
those decisions.

==================================================
1. PROJECT OVERVIEW
==================================================

This project investigates New York City restaurant food safety by
using public inspection data to identify trends, compare restaurant
patterns, and create a more interactive way to explore food safety
outcomes.

The central driving question is:

How do food safety outcomes vary across restaurants, boroughs,
cuisines, and inspection patterns in New York City, and how can
these patterns help people make safer dining decisions?

The final result is a Dash dashboard that transforms raw inspection
records into an interactive web-based visualization.

==================================================
2. MILESTONE 1
FOUNDATION: DATA UNDERSTANDING AND CLEANING
==================================================

Main purpose:
Milestone 1 focused on understanding the raw dataset and preparing
it for analysis.

What was done:
- loaded the inspection dataset
- explored the dataset structure
- reviewed columns and missing values
- standardized column names
- fixed data types for dates and numeric values
- renamed unclear columns such as boro to borough
- removed unusable or incomplete records
- removed duplicate rows

Why this was important:
The raw dataset was not immediately analysis-ready. It contained
missing values, repeated inspections, placeholder values, and
inconsistent formatting. Before building any visualizations, the
project needed a reliable and consistent data foundation.

Reasoning behind this stage:
Milestone 1 was necessary because a dashboard built on poorly
prepared data would be misleading. This stage ensured the project
started with data quality and structural clarity.

Key idea:
Milestone 1 was about making the raw data trustworthy enough for
analysis.

==================================================
3. MILESTONE 2
ANALYSIS AND EXPLORATORY VISUALIZATION
==================================================

Main purpose:
Milestone 2 focused on moving from cleaned data to interpretive
analysis and initial visual storytelling.

What was added:
- grade distribution analysis
- borough comparison visuals
- monthly score trends
- cuisine pattern exploration
- top violation summaries
- initial restaurant-level latest snapshot analysis
- early outputs saved to milestone folders

Why this was important:
Once the data was cleaned, the next step was to identify patterns.
This milestone helped determine which views were most meaningful for
the final dashboard.

Reasoning behind this stage:
Milestone 2 served as a bridge between raw analysis and final
presentation. It allowed the project to test which variables and
comparisons actually helped answer the driving question.

Key idea:
Milestone 2 was about discovering which stories in the data were
worth showing interactively later.

==================================================
4. MILESTONE 3
INTERACTIVE DASHBOARD DEVELOPMENT
==================================================

Main purpose:
Milestone 3 focused on turning the analysis into an interactive
dashboard that could be used in a browser.

What was added:
- summary KPI cards
- borough comparison chart
- trend over time chart
- cuisine risk comparison
- violation category summary
- interactive restaurant safety map
- map filtering by borough, cuisine, and restaurant name
- click-based restaurant inspection detail panel
- a safer-picks table for practical use

Feature engineering added during this stage:
- risk level created from inspection score
- latest restaurant inspection snapshot
- simplified violation categories from raw text
- cleaned labels for map and dropdowns
- time fields such as year and year-month

Why this was important:
Milestone 3 transformed the project from analysis into an
interactive data product. Instead of only reading notebook outputs,
users could explore the dashboard directly through filters, charts,
and the map.

Reasoning behind this stage:
The project moved beyond “what does the data show” and into “how can
the user interact with the data to answer the question themselves.”
That made the project more aligned with interactive data principles.

Key idea:
Milestone 3 was about turning analysis into a user-facing
interactive experience.

==================================================
5. HOW THE PROJECT EVOLVED ACROSS MILESTONES
==================================================

Milestone 1:
- focused on cleaning and structuring the dataset

Milestone 2:
- focused on exploratory analysis and identifying meaningful chart
  directions

Milestone 3:
- focused on delivering an interactive dashboard for presentation
  and practical exploration

In other words:
- Milestone 1 asked: Can the raw data be trusted and prepared?
- Milestone 2 asked: What patterns are visible in the data?
- Milestone 3 asked: How can those patterns be presented
  interactively for an audience?

==================================================
6. WHY THE FINAL PROJECT USES A DASH APP
==================================================

The notebook was useful for analysis and milestone development, but
the final dashboard required a more interactive format.

Dash was chosen because:
- it works directly in Python
- it supports interactive charts and filters
- it allows browser-based presentation through localhost
- it is suitable for converting notebook logic into a real dashboard

Reasoning:
The dashboard needed to be more than a set of screenshots. It needed
to let users filter, compare, and explore the inspection data in
real time.

==================================================
7. PROJECT STRUCTURE
==================================================

The final project is structured into layers.

Notebook layer:
- nyc_food_safety_milestone_3.ipynb
- used for milestone analysis, exploration, and development

Data layer:
- data_utils.py
- handles loading, cleaning, feature engineering, and filtering

Dashboard layer:
- app.py
- builds the dashboard layout, charts, map, and callbacks

Styling layer:
- assets/styles.css
- controls presentation and visual design

Support layer:
- requirements.txt
- README.md
- CLASS_PRESENTATION_GUIDE.txt

Why this structure matters:
It keeps the project organized and makes it easier to explain which
part of the project handles which responsibility.

==================================================
8. MAJOR DATA DECISIONS
==================================================

Some of the most important decisions in the final project were:

1. Using a cleaned inspection-level dataset for historical analysis
This keeps the time trend and violation summaries grounded in actual
inspection records.

2. Using a latest-inspection restaurant snapshot for restaurant-level
comparison
This avoids overcounting restaurants that appear many times in the
raw historical data.

3. Grouping violation descriptions into broader categories
This improves readability and helps non-technical users understand
inspection issues more easily.

4. Treating invalid values such as borough value 0 as missing
This prevents fake geographic categories from appearing in charts.

==================================================
9. DESIGN REASONING
==================================================

The final dashboard was designed for both academic and practical
audiences.

Academic audience:
- professor
- classmates
- anyone interested in the analysis process and patterns

Practical audience:
- students
- tourists
- diners
- local users who want clearer food safety signals

Design choices were made to support both groups:
- KPI cards for quick summary
- borough and trend charts for analytical interpretation
- cuisine and violation charts for pattern explanation
- map and detail panel for practical exploration

==================================================
10. LIMITATIONS
==================================================

The final project still has important limitations:

- inspection data is observational, not experimental
- some fields in the raw data were missing or invalid
- violation categories are simplified and not based on full NLP
- the dashboard focuses on what is available in the dataset, not on
  every possible factor affecting restaurant safety

These limitations do not invalidate the project, but they should be
acknowledged honestly.

==================================================
11. FUTURE IMPROVEMENTS
==================================================

Potential next steps include:

- deeper borough-over-time comparisons
- additional map interaction improvements
- more advanced violation text analysis
- public deployment after local testing is complete
- user-specific recommendation features

==================================================
12. FINAL SUBMISSION STATEMENT
==================================================

This final project began as a raw inspection dataset and developed
through three stages: cleaning and structuring the data, identifying
meaningful analytical patterns, and building a final interactive
dashboard. The final result combines data wrangling, feature
engineering, analysis, and interactive presentation into one
cohesive project that answers the driving question in a practical
and visually accessible way.
