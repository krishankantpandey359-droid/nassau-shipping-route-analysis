
from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# ==================================================
# PROJECT SETUP
# ==================================================

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "Nassau_Candy_Distributor.csv"

sys.path.insert(0, str(ROOT / "src"))
from pipeline import load_data

st.set_page_config(
    page_title="Nassau Logistics Intelligence",
    page_icon="ðŸšš",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# DESIGN
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #F3F6FB;
    color: #17263F;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #F3F6FB;
}

.block-container {
    max-width: 1550px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3, p, label {
    color: #17263F;
}

.hero {
    background: linear-gradient(115deg, #101C3A, #173B65, #087E8B);
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 22px;
    box-shadow: 0 8px 25px rgba(20,40,70,.12);
}

.hero * {
    color: #FFFFFF !important;
}

.hero .eyebrow {
    color: #8EE7DC !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero h1 {
    font-family: 'Manrope', sans-serif;
    font-size: 30px;
    font-weight: 800;
    margin: 12px 0;
}

.hero p {
    color: #E7F1FF !important;
    font-size: 15px;
}

.kpi {
    background: #FFFFFF;
    border: 1px solid #DFE6F0;
    border-radius: 14px;
    padding: 17px;
    min-height: 112px;
    box-shadow: 0 3px 12px rgba(20,40,70,.04);
}

.kpi-label {
    color: #52647D !important;
    font-size: 13px;
    font-weight: 600;
}

.kpi-value {
    color: #142746 !important;
    font-family: 'Manrope', sans-serif;
    font-size: 23px;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-note {
    color: #64748B !important;
    font-size: 11px;
    margin-top: 5px;
}

.section-heading {
    color: #142746 !important;
    font-family: 'Manrope', sans-serif;
    font-size: 23px;
    font-weight: 800;
    margin-top: 12px;
}

.section-description {
    color: #64748B !important;
    font-size: 14px;
}

div[data-testid="stSelectbox"] label {
    color: #17263F !important;
    font-weight: 700 !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 2px solid #A8B9CF !important;
    border-radius: 9px !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
    color: #17263F !important;
    -webkit-text-fill-color: #17263F !important;
}

div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #DFE6F0 !important;
    border-radius: 12px !important;
    padding: 14px !important;
}

div[data-testid="stMetric"] * {
    color: #17263F !important;
}

div[data-testid="stAlert"] {
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] {
    background: #202633 !important;
}

section[data-testid="stSidebar"] * {
    color: #F1F5F9;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #DCE4EF;
    border-radius: 10px;
}

.stDownloadButton button {
    background: #173B65 !important;
    color: #FFFFFF !important;
    border-radius: 8px;
    border: none;
}

.stDownloadButton button p {
    color: #FFFFFF !important;
}

hr {
    border-color: #DCE4EF;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def get_data():
    return load_data(DATA_PATH)


try:
    df, audit = get_data()
except Exception as error:
    st.error(f"Dataset loading failed: {error}")
    st.stop()

if df.empty:
    st.error("The dataset is empty.")
    st.stop()

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">
        NASSAU CANDY DISTRIBUTOR | LOGISTICS INTELLIGENCE
    </div>
    <h1>Factory-to-Customer Shipping Route Efficiency</h1>
    <p>
        Explore recorded lead times, route volumes, shipping modes,
        geographic summaries and data-quality findings.
    </p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR FILTERS
# ==================================================
st.sidebar.title("Dashboard Controls")
st.sidebar.caption("Filters apply across the dashboard.")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

regions = sorted(df["Region"].dropna().unique().tolist())
states = sorted(df["State/Province"].dropna().astype(str).unique().tolist())
modes = sorted(df["Ship Mode"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect(
    "Customer region", regions, default=regions
)

selected_states = st.sidebar.multiselect(
    "Customer state", states, default=states
)

selected_modes = st.sidebar.multiselect(
    "Ship mode", modes, default=modes
)

include_anomalies = st.sidebar.checkbox(
    "Include anomalous dates in diagnostic charts",
    value=True,
)

st.sidebar.markdown("---")
st.sidebar.warning(
    "All source lead times exceed the provisional 180-day threshold. "
    "Validate source dates before operational use."
)

# ==================================================
# FILTER DATA
# ==================================================

filtered = df.copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start = pd.Timestamp(date_range[0])
    end = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)

    filtered = filtered[
        (filtered["Order Date"] >= start)
        & (filtered["Order Date"] < end)
    ]

filtered = filtered[
    filtered["Region"].isin(selected_regions)
    & filtered["State/Province"].astype(str).isin(selected_states)
    & filtered["Ship Mode"].isin(selected_modes)
].copy()

filtered["Date anomaly"] = (
    filtered["Lead Time Days"].isna()
    | (filtered["Lead Time Days"] < 0)
    | (filtered["Lead Time Days"] > 180)
)

performance = filtered.copy()

if not include_anomalies:
    performance = performance[~performance["Date anomaly"]].copy()

row_count = len(filtered)
unique_orders = filtered["Order ID"].nunique()
anomaly_count = int(filtered["Date anomaly"].sum())

anomaly_pct = (
    anomaly_count / row_count * 100 if row_count else 0
)

avg_lead = performance["Lead Time Days"].mean()
sales = filtered["Sales"].sum()

# ==================================================
# KPI CARDS
# ==================================================

st.markdown("### Business Performance Overview")

kpis = [
    ("Filtered records", f"{row_count:,}", "Rows after filters"),
    ("Unique orders", f"{unique_orders:,}", "Distinct order IDs"),
    ("Date anomalies", f"{anomaly_count:,}", f"{anomaly_pct:.1f}% of filtered rows"),
    (
        "Average recorded lead time",
        f"{avg_lead:.1f} days" if pd.notna(avg_lead) else "N/A",
        "Unverified source dates",
    ),
    (
        "Recorded sales",
        f"{sales:,.0f}",
        "Currency unconfirmed; not freight cost",
    ),
]

cols = st.columns(5)

for col, (label, value, note) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)

if anomaly_count:
    st.warning(
        f"{anomaly_count:,} records have missing, negative or over-180-day "
        "lead times. Route rankings are diagnostic until source dates are validated."
    )

# ==================================================
# SECTION SELECTOR
# ==================================================

st.markdown("---")

section = st.selectbox(
    "SELECT DASHBOARD SECTION",
    [
        "Overview",
        "Route leaderboard",
        "Geographic view",
        "Ship mode analysis",
        "Order drill-down",
        "Data quality & validation",
    ],
)

# ==================================================
# OVERVIEW
# ==================================================

if section == "Overview":

    st.markdown(
        '<div class="section-heading">Operations at a glance</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">Commercial and shipment summary.</div>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("No records match the selected filters.")
    else:
        left, right = st.columns(2)

        with left:
            trend = (
                filtered.assign(
                    Month=filtered["Order Date"].dt.to_period("M").astype(str)
                )
                .groupby("Month", as_index=False)
                .agg(Orders=("Order ID", "nunique"))
            )

            fig = px.line(
                trend,
                x="Month",
                y="Orders",
                markers=True,
                title="Unique orders by order month",
                template="plotly_white",
            )

            fig.update_traces(line_color="#087E8B", line_width=3)
            fig.update_layout(font_color="#17263F")
            st.plotly_chart(fig, width='stretch')

        with right:
            division = (
                filtered.groupby("Division", as_index=False)
                .agg(Sales=("Sales", "sum"))
            )

            if not division.empty:
                fig = px.pie(
                    division,
                    names="Division",
                    values="Sales",
                    hole=0.55,
                    title="Recorded sales by division",
                    template="plotly_white",
                )

                fig.update_layout(font_color="#17263F")
                st.plotly_chart(fig, width='stretch')

    st.markdown("### Business snapshot")

    snapshot = pd.DataFrame({
        "Metric": [
            "Recorded sales",
            "Recorded gross profit",
            "Units",
            "Customer states",
            "Ship modes",
        ],
        "Value": [
            f"{filtered['Sales'].sum():,.2f}",
            f"{filtered['Gross Profit'].sum():,.2f}",
            f"{filtered['Units'].sum():,.0f}",
            str(filtered["State/Province"].nunique()),
            str(filtered["Ship Mode"].nunique()),
        ],
    })

    st.dataframe(snapshot, hide_index=True, width='stretch')

    st.info(
        "Sales and gross profit are commercial measures, not freight costs. "
        "Customer coordinates are not supplied, so road distances are unavailable."
    )

# ==================================================
# ROUTE LEADERBOARD
# ==================================================

elif section == "Route leaderboard":

    st.markdown(
        '<div class="section-heading">Route diagnostics leaderboard</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Route = Factory â†’ Customer State. "
        "Factory is inferred from the supplied product mapping."
    )

    if performance.empty:
        st.warning(
            "No records are available for diagnostic route analysis. "
            "Enable anomalous dates in the sidebar to inspect the source records."
        )
    else:
        ranking = st.radio(
            "Rank routes by",
            [
                "Average lead time",
                "Unique order volume",
                "Lead-time variability",
            ],
            horizontal=True,
        )

        routes = (
            performance.groupby(
                ["Factory", "State/Province", "Region", "Route"],
                as_index=False,
            )
            .agg(
                Unique_orders=("Order ID", "nunique"),
                Average_lead_time=("Lead Time Days", "mean"),
                Lead_time_std=("Lead Time Days", "std"),
                Recorded_sales=("Sales", "sum"),
            )
        )

        if ranking == "Average lead time":
            routes = routes.sort_values("Average_lead_time")
        elif ranking == "Unique order volume":
            routes = routes.sort_values(
                "Unique_orders", ascending=False
            )
        else:
            routes = routes.sort_values(
                "Lead_time_std", ascending=False
            )

        st.dataframe(
            routes.round(2),
            hide_index=True,
            width='stretch',
        )

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("### 10 lowest recorded lead-time routes")
            st.dataframe(
                routes.sort_values("Average_lead_time")
                .head(10).round(2),
                hide_index=True,
                width='stretch',
            )

        with c2:
            st.markdown("### 10 highest recorded lead-time routes")
            st.dataframe(
                routes.sort_values(
                    "Average_lead_time", ascending=False
                ).head(10).round(2),
                hide_index=True,
                width='stretch',
            )

        st.warning(
            "Recorded-date diagnostics only. Source dates are unverified. "
            "Do not interpret these rankings as actual shipping efficiency."
        )

# ==================================================
# GEOGRAPHIC VIEW
# ==================================================

elif section == "Geographic view":

    st.markdown(
        '<div class="section-heading">Geographic shipping analysis</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Customer coordinates are unavailable. Charts use customer state summaries."
    )

    geo = (
        filtered.groupby(
            ["State/Province", "Region"], as_index=False
        )
        .agg(
            Unique_orders=("Order ID", "nunique"),
            Recorded_sales=("Sales", "sum"),
            Average_recorded_lead_time=("Lead Time Days", "mean"),
        )
    )

    if geo.empty:
        st.info("No records match the selected filters.")
    else:
        fig = px.bar(
            geo.sort_values(
                "Unique_orders", ascending=False
            ).head(25),
            x="State/Province",
            y="Unique_orders",
            color="Region",
            title="Customer states by unique orders",
            template="plotly_white",
        )

        fig.update_layout(
            xaxis_tickangle=-40,
            font_color="#17263F",
        )

        st.plotly_chart(fig, width='stretch')

        st.markdown("### State summary")

        st.dataframe(
            geo.sort_values(
                "Unique_orders", ascending=False
            ).round(2),
            hide_index=True,
            width='stretch',
        )

# ==================================================
# SHIP MODE ANALYSIS
# ==================================================

elif section == "Ship mode analysis":

    st.markdown(
        '<div class="section-heading">Ship mode comparison</div>',
        unsafe_allow_html=True,
    )

    mode = (
        filtered.groupby("Ship Mode", as_index=False)
        .agg(
            Unique_orders=("Order ID", "nunique"),
            Average_recorded_lead_time=("Lead Time Days", "mean"),
            Lead_time_std=("Lead Time Days", "std"),
            Recorded_sales=("Sales", "sum"),
        )
    )

    if mode.empty:
        st.info("No records match the selected filters.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            fig = px.bar(
                mode,
                x="Ship Mode",
                y="Unique_orders",
                color="Ship Mode",
                title="Unique orders by ship mode",
                template="plotly_white",
            )

            fig.update_layout(
                showlegend=False,
                font_color="#17263F",
            )

            st.plotly_chart(fig, width='stretch')

        with c2:
            fig = px.bar(
                mode,
                x="Ship Mode",
                y="Average_recorded_lead_time",
                color="Ship Mode",
                title="Average recorded lead time",
                template="plotly_white",
            )

            fig.update_layout(
                showlegend=False,
                font_color="#17263F",
            )

            st.plotly_chart(fig, width='stretch')

        st.dataframe(
            mode.round(2),
            hide_index=True,
            width='stretch',
        )

        st.warning(
            "Source date anomalies prevent reliable service-speed comparisons. "
            "Do not interpret recorded lead times as actual service performance."
        )

# ==================================================
# ORDER DRILL-DOWN
# ==================================================

elif section == "Order drill-down":

    st.markdown(
        '<div class="section-heading">Order-level drill-down</div>',
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "Search order, customer, city, product or state"
    )

    detail = filtered.copy()

    if search.strip():
        query = search.strip().lower()

        search_cols = [
            "Order ID",
            "Customer ID",
            "City",
            "Product Name",
            "State/Province",
        ]

        mask = detail[search_cols].astype(str).apply(
            lambda col: col.str.lower().str.contains(
                query, regex=False, na=False
            )
        ).any(axis=1)

        detail = detail[mask]

    columns = [
        "Order ID",
        "Order Date",
        "Ship Date",
        "Lead Time Days",
        "Date anomaly",
        "Ship Mode",
        "Factory",
        "City",
        "State/Province",
        "Region",
        "Product Name",
        "Sales",
        "Gross Profit",
    ]

    st.dataframe(
        detail[columns].head(500),
        hide_index=True,
        width='stretch',
    )

    st.caption(
        f"Showing {min(len(detail), 500):,} of {len(detail):,} matching rows."
    )

# ==================================================
# DATA QUALITY AND VALIDATION
# ==================================================

elif section == "Data quality & validation":

    st.markdown(
        '<div class="section-heading">Data quality & validation</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "Source values are preserved. The 180-day cutoff is a provisional "
        "screening rule, not a contractual delivery SLA."
    )

    a, b, c = st.columns(3)

    a.metric("Source rows", f"{len(df):,}")
    b.metric(
        "Date anomaly rows",
        f"{int(df['Date anomaly'].sum()):,}",
    )
    c.metric(
        "Anomaly percentage",
        f"{df['Date anomaly'].mean() * 100:.1f}%",
    )

    checks = [
        ("Row count", audit.get("rows", len(df)), "Source records loaded"),
        ("Source columns", audit.get("source_columns", 0), "Required source fields"),
        ("Missing source values", audit.get("source_missing_cells", 0), "Across required columns"),
        ("Duplicate Row IDs", audit.get("duplicate_row_ids", 0), "Expected to be zero"),
        ("Duplicate Order IDs", audit.get("duplicate_order_ids", 0), "May represent multi-product orders"),
        ("Invalid order dates", audit.get("invalid_order_dates", 0), "Could not be parsed"),
        ("Invalid ship dates", audit.get("invalid_ship_dates", 0), "Could not be parsed"),
        ("Negative lead times", audit.get("negative_lead_times", 0), "Ship date before order date"),
        ("Lead time over 180 days", audit.get("over_180_day_lead_times", 0), "Provisional threshold, not an SLA"),
        ("Unmapped products", audit.get("unmapped_products", 0), "No factory assigned"),
    ]

    quality = pd.DataFrame(
        checks,
        columns=[
            "Validation check",
            "Count",
            "Interpretation",
        ],
    )

    st.markdown("### Validation results")

    st.dataframe(
        quality,
        hide_index=True,
        width='stretch',
    )

    st.markdown("### Source date ranges")

    c1, c2 = st.columns(2)

    c1.info(
        f"Order dates: {df['Order Date'].min().date()} "
        f"to {df['Order Date'].max().date()}"
    )

    c2.info(
        f"Ship dates: {df['Ship Date'].min().date()} "
        f"to {df['Ship Date'].max().date()}"
    )

    st.markdown("### Lead-time distribution")

    lead = df["Lead Time Days"].dropna()

    if not lead.empty:
        st.write(
            f"Minimum: {lead.min():,.0f} days | "
            f"Median: {lead.median():,.0f} days | "
            f"Maximum: {lead.max():,.0f} days"
        )

        fig = px.histogram(
            df,
            x="Lead Time Days",
            nbins=40,
            title="Recorded lead-time distribution",
            template="plotly_white",
        )

        fig.update_layout(font_color="#17263F")

        st.plotly_chart(fig, width='stretch')

    st.markdown("### Export reports")

    st.download_button(
        "Download filtered CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="nassau_filtered_shipments.csv",
        mime="text/csv",
    )

    st.download_button(
        "Download data quality report",
        data=quality.to_csv(index=False).encode("utf-8"),
        file_name="nassau_data_quality_report.csv",
        mime="text/csv",
    )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Nassau Candy Distributor | Logistics Analytics Portfolio Project | "
    "Validate source dates before operational recommendations."
)

