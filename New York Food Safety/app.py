from __future__ import annotations

from dash import Dash, Input, Output, dash_table, dcc, html
import plotly.express as px
import plotly.graph_objects as go

from data_utils import apply_filters, load_data_bundle


# ============================================================
# Chunk 1: Visual constants and shared chart settings
# Why this exists:
# This section keeps the dashboard's colors and plotting defaults
# consistent across every chart so the interface feels unified.
# ============================================================
SAFE_GREEN = "#2E8B57"
CAUTION_AMBER = "#D7A229"
ALERT_RED = "#C7522A"
INFO_BLUE = "#2B5F75"
SLATE = "#30404D"
LINE = "#D9D2C3"
CARD = "#FFFDF8"

RISK_COLORS = {"Low": SAFE_GREEN, "Medium": CAUTION_AMBER, "High": ALERT_RED}

PLOT_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor=CARD,
    plot_bgcolor=CARD,
    font=dict(color=SLATE, family='"Avenir Next", "Helvetica Neue", Arial, sans-serif'),
)


bundle = load_data_bundle()
app = Dash(__name__, title="NYC Food Safety Dashboard")
server = app.server


# ============================================================
# Chunk 2: Reusable UI helper components
# Why this exists:
# These helper functions reduce repetition in the layout and make
# the dashboard easier to maintain and explain.
# ============================================================
def metric_card(title: str, metric_id: str, tone: str) -> html.Div:
    return html.Div(
        className=f"metric-card tone-{tone}",
        children=[
            html.Div(title, className="metric-title"),
            html.Div(id=metric_id, className="metric-value"),
        ],
    )


def filter_dropdown(filter_id: str, label: str, options: list[str], value: str) -> html.Div:
    return html.Div(
        className="filter-field",
        children=[
            html.Label(label),
            dcc.Dropdown(
                id=filter_id,
                options=[{"label": x, "value": x} for x in options],
                value=value,
                clearable=False,
                searchable=True,
                className="clean-dropdown",
            ),
        ],
    )


def chart_card(title: str, graph_id: str, extra_class: str = "") -> html.Section:
    class_name = "chart-card" if not extra_class else f"chart-card {extra_class}"
    return html.Section(
        className=class_name,
        children=[
            html.Div(className="section-header", children=[html.H3(title)]),
            dcc.Graph(id=graph_id, config={"displayModeBar": False}),
        ],
    )


# ============================================================
# Chunk 3: Shared figure typography helper
# Why this exists:
# Instead of styling every figure separately, this helper applies
# a consistent title, axis, legend, and hover style.
# ============================================================
def apply_chart_typography(fig, *, height: int, margin: dict, xaxis_title: str | None = None,
                           yaxis_title: str | None = None, legend_orientation: str = "h"):
    fig.update_layout(
        **PLOT_LAYOUT,
        height=height,
        margin=margin,
        title=dict(
            x=0.02,
            xanchor="left",
            font=dict(
                family='"Palatino Linotype", "Book Antiqua", Georgia, serif',
                size=22,
                color=SLATE,
            ),
        ),
        legend=dict(
            orientation=legend_orientation,
            yanchor="bottom",
            y=1.02 if legend_orientation == "h" else 1,
            xanchor="center" if legend_orientation == "h" else "left",
            x=0.5 if legend_orientation == "h" else 1.02,
            font=dict(size=12, family='"Avenir Next", "Helvetica Neue", Arial, sans-serif'),
            title=dict(font=dict(size=12)),
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family='"Avenir Next", "Helvetica Neue", Arial, sans-serif',
        ),
    )
    fig.update_xaxes(
        title=xaxis_title,
        title_font=dict(size=13, family='"Avenir Next", "Helvetica Neue", Arial, sans-serif'),
        tickfont=dict(size=11, family='"Avenir Next", "Helvetica Neue", Arial, sans-serif'),
        automargin=True,
    )
    fig.update_yaxes(
        title=yaxis_title,
        title_font=dict(size=13, family='"Avenir Next", "Helvetica Neue", Arial, sans-serif'),
        tickfont=dict(size=11, family='"Avenir Next", "Helvetica Neue", Arial, sans-serif'),
        automargin=True,
    )
    return fig


# ============================================================
# Chunk 4: Dashboard layout
# Why this exists:
# This is the visible structure of the app: title, filters, KPI
# cards, analytical charts, map, and table.
# ============================================================
app.layout = html.Div(
    className="app-shell",
    children=[
        html.Div(className="hero-glow hero-left"),
        html.Div(className="hero-glow hero-right"),
        html.Header(
            className="hero-simple",
            children=[
                html.P("New York Food Safety", className="eyebrow"),
                html.H1("Interactive Inspection Dashboard"),
            ],
        ),
        html.Section(
            className="filters-panel compact-panel",
            children=[
                html.Div(className="section-header", children=[html.H2("Dashboard Filters")]),
                html.Div(
                    className="filters-grid filters-grid-compact",
                    children=[
                        filter_dropdown(
                            "cuisine-filter",
                            "Restaurant Type",
                            bundle.cuisine_options,
                            "All Restaurant Types",
                        ),
                        filter_dropdown(
                            "grade-filter",
                            "Grade",
                            bundle.grade_options,
                            "All Grades",
                        ),
                    ],
                ),
            ],
        ),
        html.Section(
            className="metrics-grid",
            children=[
                metric_card("Restaurants in view", "metric-restaurants", "neutral"),
                metric_card("A grade share", "metric-grade", "safe"),
                metric_card("Average score", "metric-score", "info"),
                metric_card("Critical violation share", "metric-critical", "alert"),
            ],
        ),
        html.Section(
            className="charts-grid",
            children=[
                chart_card("Borough Comparison", "borough-chart", "chart-wide"),
                chart_card("Inspection Trend Over Time", "trend-chart"),
                chart_card("Cuisine Risk Landscape", "cuisine-chart"),
                chart_card("Violation Category Summary", "violation-chart", "chart-wide"),
            ],
        ),
        html.Section(
            className="chart-card map-card",
            children=[
                html.Div(className="section-header", children=[html.H3("NYC Restaurant Safety Map")]),
                html.Div(
                    className="filters-grid map-filter-grid",
                    children=[
                        filter_dropdown(
                            "map-borough-filter",
                            "Map Borough",
                            [option for option in bundle.borough_options if option != "Not Reported"],
                            "All Boroughs",
                        ),
                        filter_dropdown(
                            "map-cuisine-filter",
                            "Map Cuisine",
                            bundle.cuisine_options,
                            "All Restaurant Types",
                        ),
                        html.Div(
                            className="filter-field restaurant-field",
                            children=[
                                html.Label("Restaurant Name"),
                                dcc.Dropdown(
                                    id="map-restaurant-filter",
                                    options=[
                                        {"label": x, "value": x}
                                        for x in bundle.restaurant_options
                                    ],
                                    value="All Restaurants",
                                    clearable=False,
                                    searchable=True,
                                    placeholder="Search restaurant by name",
                                    className="clean-dropdown",
                                ),
                            ],
                        ),
                    ],
                ),
                dcc.Graph(id="map-chart", config={"displayModeBar": False}),
                html.Div(
                    id="inspection-detail-card",
                    className="inspection-detail-card",
                    children=[
                        html.H4("Inspection Comment"),
                        html.P(
                            "Click a restaurant circle on the map to see the full inspection comment here."
                        ),
                    ],
                ),
            ],
        ),
        html.Section(
            className="chart-card",
            children=[
                html.Div(className="section-header", children=[html.H3("Quick Safer Picks")]),
                dash_table.DataTable(
                    id="safer-picks-table",
                    columns=[
                        {"name": "Restaurant", "id": "dba"},
                        {"name": "Borough", "id": "borough"},
                        {"name": "Cuisine", "id": "cuisine_description"},
                        {"name": "Grade", "id": "grade"},
                        {"name": "Score", "id": "score"},
                        {"name": "Inspection Date", "id": "inspection_date"},
                    ],
                    page_size=10,
                    sort_action="native",
                    style_table={"overflowX": "auto"},
                    style_header={
                        "backgroundColor": SAFE_GREEN,
                        "color": "white",
                        "fontWeight": "bold",
                        "border": "none",
                    },
                    style_cell={
                        "backgroundColor": CARD,
                        "color": SLATE,
                        "border": f"1px solid {LINE}",
                        "padding": "10px",
                        "textAlign": "left",
                        "fontFamily": "Georgia, Cambria, serif",
                    },
                ),
            ],
        ),
    ],
)


# ============================================================
# Chunk 5: Main callback for interactivity
# Why this exists:
# Dash uses callbacks to update outputs when a user changes a
# filter or clicks on the map. This is the core interactive
# engine of the dashboard.
# ============================================================
@app.callback(
    Output("metric-restaurants", "children"),
    Output("metric-grade", "children"),
    Output("metric-score", "children"),
    Output("metric-critical", "children"),
    Output("borough-chart", "figure"),
    Output("trend-chart", "figure"),
    Output("cuisine-chart", "figure"),
    Output("violation-chart", "figure"),
    Output("map-chart", "figure"),
    Output("safer-picks-table", "data"),
    Output("inspection-detail-card", "children"),
    Input("cuisine-filter", "value"),
    Input("grade-filter", "value"),
    Input("map-borough-filter", "value"),
    Input("map-cuisine-filter", "value"),
    Input("map-restaurant-filter", "value"),
    Input("map-chart", "clickData"),
)
def update_dashboard(
    cuisine: str,
    grade: str,
    map_borough: str,
    map_cuisine: str,
    map_restaurant: str,
    map_click_data: dict | None,
):
    usable, latest = apply_filters(
        bundle.usable,
        bundle.latest,
        "All Boroughs",
        cuisine,
        grade,
        "All Risk Levels",
    )

    restaurants_count = latest["camis"].nunique()
    grade_a_pct = latest["grade"].eq("A").mean() * 100 if len(latest) else 0
    avg_score = latest["score"].mean() if len(latest) else 0
    critical_pct = latest["has_critical_violation"].mean() * 100 if len(latest) else 0

    # ------------------------------------------------------------
    # Chunk 5A: Borough comparison chart
    # Purpose:
    # Compare boroughs using average score and critical violation
    # rate from the latest restaurant-level inspection snapshot.
    # ------------------------------------------------------------
    borough_summary = (
        latest.groupby("borough_clean", as_index=False)
        .agg(
            avg_score=("score", "mean"),
            restaurant_count=("camis", "nunique"),
            critical_rate=("has_critical_violation", "mean"),
        )
        .sort_values("avg_score", ascending=True)
    )
    borough_summary = borough_summary[borough_summary["borough_clean"] != "Not Reported"].copy()
    borough_summary["critical_rate"] = borough_summary["critical_rate"] * 100

    borough_fig = go.Figure()
    borough_fig.add_trace(
        go.Bar(
            x=borough_summary["borough_clean"],
            y=borough_summary["avg_score"],
            name="Average Inspection Score",
            marker=dict(
                color=INFO_BLUE,
                line=dict(color=CARD, width=1.0),
            ),
            customdata=borough_summary[["restaurant_count", "critical_rate"]],
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Average score: %{y:.2f}<br>"
                "Restaurants: %{customdata[0]:,}<br>"
                "Critical violation rate: %{customdata[1]:.1f}%<extra></extra>"
            ),
        )
    )
    borough_fig.add_trace(
        go.Scatter(
            x=borough_summary["borough_clean"],
            y=borough_summary["critical_rate"],
            name="Critical Violation Rate (%)",
            mode="lines+markers",
            yaxis="y2",
            line=dict(color=INFO_BLUE, width=3),
            marker=dict(size=9, color=INFO_BLUE),
            hovertemplate="<b>%{x}</b><br>Critical violation rate: %{y:.1f}%<extra></extra>",
        )
    )
    borough_fig.update_layout(
        title="Borough Comparison: Score and Critical Violations",
        hovermode="x unified",
        xaxis=dict(title="Borough"),
        yaxis=dict(
            title="Average Inspection Score (Lower = Better)",
            gridcolor=LINE,
            zeroline=False,
        ),
        yaxis2=dict(
            title="Critical Violation Rate (%)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
    )
    apply_chart_typography(
        borough_fig,
        height=500,
        margin=dict(l=50, r=60, t=78, b=42),
        xaxis_title="Borough",
        yaxis_title="Average Inspection Score (Lower = Better)",
    )

    # ------------------------------------------------------------
    # Chunk 5B: Trend chart
    # Purpose:
    # Show how average inspection score changes over time so the
    # dashboard is not limited to a single static snapshot.
    # ------------------------------------------------------------
    monthly_trend = (
        usable.dropna(subset=["score"])
        .groupby("year_month", as_index=False)
        .agg(avg_score=("score", "mean"), inspections=("camis", "count"))
    )
    monthly_trend = monthly_trend[monthly_trend["year_month"] >= "2018-01"].copy()
    trend_fig = px.line(
        monthly_trend,
        x="year_month",
        y="avg_score",
        markers=True,
        title="Average Inspection Score Over Time",
    )
    trend_fig.update_traces(
        line=dict(color=INFO_BLUE, width=3),
        marker=dict(color=INFO_BLUE, size=6),
        hovertemplate="<b>%{x}</b><br>Average score: %{y:.2f}<extra></extra>",
    )
    apply_chart_typography(
        trend_fig,
        height=500,
        margin=dict(l=40, r=30, t=78, b=62),
        xaxis_title="Year-Month",
        yaxis_title="Average Score (Lower = Better)",
    )

    # ------------------------------------------------------------
    # Chunk 5C: Cuisine landscape chart
    # Purpose:
    # Compare restaurant types using both average score and
    # critical violation rate in a single visual.
    # ------------------------------------------------------------
    cuisine_summary = (
        latest.groupby("cuisine_clean", as_index=False)
        .agg(
            restaurants=("camis", "nunique"),
            avg_score=("score", "mean"),
            critical_rate=("has_critical_violation", "mean"),
        )
    )
    cuisine_summary["critical_rate"] = cuisine_summary["critical_rate"] * 100
    cuisine_summary = cuisine_summary[cuisine_summary["restaurants"] >= 15].copy()
    cuisine_summary = cuisine_summary.sort_values(
        ["critical_rate", "restaurants"], ascending=[False, False]
    ).head(18)

    cuisine_fig = px.scatter(
        cuisine_summary,
        x="avg_score",
        y="critical_rate",
        size="restaurants",
        color="critical_rate",
        hover_name="cuisine_clean",
        color_continuous_scale=[[0, SAFE_GREEN], [0.5, CAUTION_AMBER], [1, ALERT_RED]],
        size_max=38,
        title="Cuisine Risk Landscape",
    )
    cuisine_fig.update_traces(
        marker=dict(line=dict(color=CARD, width=1.2), opacity=0.88),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Average score: %{x:.2f}<br>"
            "Critical violation rate: %{y:.1f}%<br>"
            "Restaurants: %{marker.size:.0f}<extra></extra>"
        ),
    )
    cuisine_fig.update_layout(coloraxis_colorbar=dict(title="Critical %"))
    apply_chart_typography(
        cuisine_fig,
        height=500,
        margin=dict(l=50, r=40, t=78, b=52),
        xaxis_title="Average Inspection Score",
        yaxis_title="Critical Violation Rate (%)",
    )

    # ------------------------------------------------------------
    # Chunk 5D: Violation category chart
    # Purpose:
    # Summarize which high-level food safety issues appear most
    # often in the inspection records.
    # ------------------------------------------------------------
    category_counts = (
        usable["violation_category"].value_counts().reset_index()
        .rename(columns={"index": "violation_category", "violation_category": "count"})
    )
    category_counts.columns = ["violation_category", "count"]
    total_violation_records = int(category_counts["count"].sum())
    category_counts["share_pct"] = category_counts["count"] / total_violation_records * 100
    category_counts = category_counts.sort_values("count", ascending=True)
    top_violation = category_counts.iloc[-1]

    violation_fig = px.bar(
        category_counts,
        x="count",
        y="violation_category",
        orientation="h",
        color="share_pct",
        color_continuous_scale=[[0.0, SAFE_GREEN], [0.5, CAUTION_AMBER], [1.0, ALERT_RED]],
        text="share_pct",
        title="Violation Category Summary",
    )
    violation_fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Inspection records: %{x:,}<br>"
            "Share of inspection records: %{marker.color:.1f}%<extra></extra>"
        ),
    )
    violation_fig.update_layout(
        annotations=[
            dict(
                x=0,
                y=1.12,
                xref="paper",
                yref="paper",
                showarrow=False,
                align="left",
                text=(
                    f"Top issue: <b>{top_violation['violation_category']}</b> "
                    f"with {int(top_violation['count']):,} inspection records "
                    f"({top_violation['share_pct']:.1f}%). "
                    "Records here mean inspection rows, not unique restaurants."
                ),
                font=dict(
                    size=12,
                    color=SLATE,
                    family='"Avenir Next", "Helvetica Neue", Arial, sans-serif',
                ),
            )
        ],
        coloraxis_colorbar=dict(title="Share %"),
    )
    apply_chart_typography(
        violation_fig,
        height=540,
        margin=dict(l=30, r=70, t=110, b=30),
        xaxis_title="Inspection Records",
        yaxis_title="Violation Category",
    )

    # ------------------------------------------------------------
    # Chunk 5E: Interactive map
    # Purpose:
    # Connect location, score, grade, and violation summary in
    # a single exploratory view for restaurant-level decisions.
    # ------------------------------------------------------------
    map_latest = latest[
        latest["latitude"].between(40.45, 40.95)
        & latest["longitude"].between(-74.30, -73.65)
    ].copy()
    map_latest = map_latest[map_latest["borough_clean"] != "Not Reported"]
    if map_borough != "All Boroughs":
        map_latest = map_latest[map_latest["borough_clean"] == map_borough]
    if map_cuisine != "All Restaurant Types":
        map_latest = map_latest[map_latest["cuisine_clean"] == map_cuisine]
    if map_restaurant != "All Restaurants":
        map_latest = map_latest[map_latest["restaurant_name"] == map_restaurant]

    map_fig = px.scatter_map(
        map_latest,
        lat="latitude",
        lon="longitude",
        color="risk_level",
        color_discrete_map=RISK_COLORS,
        custom_data=[
            "restaurant_name",
            "borough_clean",
            "cuisine_clean",
            "grade",
            "score",
            "inspection_day",
            "risk_level",
            "violation_category",
            "violation_description",
            "building",
            "street",
            "zipcode",
        ],
        zoom=9.7,
        height=700,
        title="Latest Restaurant Safety Snapshot Across NYC",
    )
    map_fig.update_traces(
        marker={
            "size": 10,
            "opacity": 0.82,
            "allowoverlap": True,
        },
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Borough: %{customdata[1]}<br>"
            "Cuisine: %{customdata[2]}<br>"
            "Grade: %{customdata[3]}<br>"
            "Score: %{customdata[4]:.0f}<br>"
            "Inspection date: %{customdata[5]}<br>"
            "Risk level: %{customdata[6]}<br>"
            "Violation summary: %{customdata[7]}<extra></extra>"
        ),
    )
    map_fig.update_layout(
        **PLOT_LAYOUT,
        margin=dict(l=10, r=10, t=78, b=10),
        title=dict(
            x=0.02,
            xanchor="left",
            font=dict(
                family='"Palatino Linotype", "Book Antiqua", Georgia, serif',
                size=22,
                color=SLATE,
            ),
        ),
        legend_title_text="Risk Level",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12, family='"Avenir Next", "Helvetica Neue", Arial, sans-serif'),
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family='"Avenir Next", "Helvetica Neue", Arial, sans-serif',
        ),
        mapbox_style="open-street-map",
    )

    # ------------------------------------------------------------
    # Chunk 5F: Click-to-view inspection detail panel
    # Purpose:
    # When a restaurant is clicked on the map, show a cleaner
    # inspection summary panel below the map.
    # ------------------------------------------------------------
    inspection_detail_children = [
        html.H4("Inspection Comment"),
        html.P("Click a restaurant circle on the map to see the full inspection comment here."),
    ]
    if map_click_data and map_click_data.get("points"):
        point = map_click_data["points"][0]
        custom = point.get("customdata", [])
        if len(custom) >= 12:
            address_parts = [str(part).strip() for part in [custom[9], custom[10], custom[11]] if str(part).strip() and str(part).strip().lower() != "nan"]
            address_text = ", ".join(address_parts) if address_parts else "Address not reported"
            inspection_detail_children = [
                html.Div(
                    className="detail-badge-row",
                    children=[
                        html.Span("Selected Restaurant", className="detail-badge"),
                    ],
                ),
                html.H4(custom[0]),
                html.Div(
                    className="detail-meta-grid",
                    children=[
                        html.Div([html.Strong("Borough"), html.Span(custom[1])]),
                        html.Div([html.Strong("Cuisine"), html.Span(custom[2])]),
                        html.Div([html.Strong("Grade"), html.Span(custom[3])]),
                        html.Div([html.Strong("Score"), html.Span(str(custom[4]))]),
                        html.Div([html.Strong("Address"), html.Span(address_text)], className="detail-address-card"),
                    ],
                ),
                html.Div(
                    className="detail-summary-box",
                    children=[
                        html.Span("Violation Summary", className="detail-label"),
                        html.P(custom[7]),
                    ],
                ),
                html.Div(
                    className="detail-comment-box",
                    children=[
                        html.Span("Full Inspection Comment", className="detail-label"),
                        html.P(custom[8]),
                    ],
                ),
            ]

    # ------------------------------------------------------------
    # Chunk 5G: Safer picks table
    # Purpose:
    # Translate analysis into a practical list of restaurants
    # with strong recent safety indicators.
    # ------------------------------------------------------------
    quick_picks = latest[
        (latest["grade"] == "A")
        & (latest["risk_level"] == "Low")
        & (~latest["has_critical_violation"])
    ].copy()
    quick_picks = quick_picks.sort_values(["score", "inspection_date"], ascending=[True, False])
    quick_picks["inspection_date"] = quick_picks["inspection_date"].dt.strftime("%Y-%m-%d")
    table_data = (
        quick_picks[
            ["dba", "borough_clean", "cuisine_clean", "grade", "score", "inspection_date"]
        ]
        .rename(
            columns={
                "borough_clean": "borough",
                "cuisine_clean": "cuisine_description",
            }
        )
        .head(20)
        .to_dict("records")
    )

    return (
        f"{restaurants_count:,}",
        f"{grade_a_pct:.1f}%",
        f"{avg_score:.2f}",
        f"{critical_pct:.1f}%",
        borough_fig,
        trend_fig,
        cuisine_fig,
        violation_fig,
        map_fig,
        table_data,
        inspection_detail_children,
    )


# ============================================================
# Chunk 6: Local app runner
# Why this exists:
# This starts the Dash server on localhost so the app can be
# viewed in the browser during development or presentation.
# ============================================================
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
