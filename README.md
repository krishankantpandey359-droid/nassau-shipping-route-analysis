# Nassau Candy Distributor
## Factory-to-Customer Shipping Route Efficiency Analysis

An interactive Streamlit dashboard and reproducible Python data pipeline developed for the Unified Mentor Data Analytics Project.

The project analyzes order records, factory-to-customer route assignments, shipping modes, geographic distribution, recorded lead times, and source-data quality.

## 1. Project Overview

This project uses Python, Pandas, NumPy, Plotly, and Streamlit to analyze the Nassau Candy Distributor dataset.

The analysis focuses on:

- Order and sales trends.
- Factory-to-customer state-level route summaries.
- Shipping mode comparisons.
- Geographic order distribution.
- Order-level data exploration.
- Data quality and date anomaly validation.

## 2. Start the Project on Windows

Open the existing `Nassau_Shipping_Route_Analysis` folder in VS Code.

Open Terminal → New Terminal.

Run:

```powershell
.\RUN_PROJECT.bat
```

Wait for the application to start. Streamlit will display a local URL, usually:

`http://localhost:8501`

Open this URL in your browser.

Keep the terminal open while using the dashboard. Press `Ctrl + C` to stop the application.

Requirements:

- Python 3.10 or newer.
- Internet connection for the initial dependency installation.
- VS Code or another Python-compatible editor.

The launcher creates and reuses the project's `.venv` environment.

## 3. Install Dependencies Manually

If you need to install the dependencies manually, run:

```powershell
python -m pip install -r requirements.txt
```

Start the dashboard using:

```powershell
python -m streamlit run app.py
```

## 4. Automated Quality Checks

Run the pipeline tests:

```powershell
python -m unittest discover -s tests -v
```

The current test suite contains five tests covering:

1. Product-to-factory mapping.
2. Date anomaly preservation.
3. Expected dataset size.
4. Lead-time calculation.
5. Unique Row IDs.

All five tests passed during the latest recorded validation.

## 5. Dashboard Features

### Overview
- Total filtered records.
- Unique order count.
- Date anomaly count.
- Average recorded lead time.
- Recorded sales.
- Monthly order trends.
- Division-wise sales distribution.

### Route Leaderboard
- Factory-to-customer-state route summaries.
- Unique order volume.
- Average recorded lead time.
- Lead-time variability.
- Route-level diagnostic rankings.

Factory assignments are inferred from the supplied product mapping.

### Geographic View
- State-level order distribution.
- Regional comparisons.
- Recorded sales summaries.

Customer coordinates are unavailable, so this is not an exact geographic routing analysis.

### Ship Mode Analysis
- Unique orders by shipping mode.
- Average recorded lead time.
- Lead-time variability.
- Descriptive shipping mode comparisons.

### Order Drill-down
- Search by order ID.
- Search by customer ID.
- Search by city, product, or state.
- View order dates, ship dates, lead times, factories, and commercial values.

### Data Quality and Validation
- Source row and column checks.
- Missing-value checks.
- Duplicate identifier checks.
- Invalid date checks.
- Negative lead-time checks.
- Over-180-day lead-time checks.
- Unmapped product checks.
- CSV report exports.

## 6. Important Source-Data Finding

The supplied dataset contains:

- 10,194 records.
- 18 source columns.
- 15 distinct products.
- No missing source values.
- No duplicate full rows.
- No duplicate Row IDs.

The source dates parse using the day-month-year format.

| Date field | Recorded range |
|---|---|
| Order Date | 2 January 2024 to 31 December 2025 |
| Ship Date | 30 June 2026 to 28 June 2030 |
| Lead Time | 904 to 1,642 days |

All 10,194 records exceed the provisional 180-day lead-time screening threshold.

The median recorded lead time is 1,274 days.

### Data Integrity Notice

The source dates are preserved. The pipeline does not silently modify or fabricate date corrections.

The 180-day threshold is a provisional screening rule, not a contractual delivery SLA.

Route rankings and shipping-mode lead-time comparisons are diagnostic only. They must not be interpreted as verified operational shipping performance until the data owner confirms or corrects the source date fields.

## 7. Project Scope and Limitations

1. Factory assignments are inferred from the product-to-factory mapping supplied in the project brief.
2. Factory assignments are derived fields, not original CSV columns.
3. Customer latitude and longitude are unavailable.
4. Geographic analysis is limited to customer-state summaries.
5. Exact road distances and route optimization are not calculated.
6. Sales and gross profit are commercial measures, not freight costs.
7. Actual transportation expenses are unavailable.
8. Shipping mode comparisons are descriptive, not causal.
9. Recorded lead times remain unverified because of the source-date anomaly.

## 8. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and pipeline |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical operations |
| Plotly | Interactive visualizations |
| Streamlit | Interactive dashboard |
| Unittest | Automated testing |
| CSV | Source data and report exports |

## 9. Project Structure

```text
Nassau_Shipping_Route_Analysis/
│
├── app.py
├── requirements.txt
├── README.md
├── DATA_DICTIONARY.md
├── RUN_COMMAND.txt
├── RUN_PROJECT.bat
├── .gitignore
│
├── data/
│   └── Nassau_Candy_Distributor.csv
│
├── src/
│   └── pipeline.py
│
├── tests/
│   └── test_pipeline.py
│
├── reports/
│   ├── Executive_Summary.md
│   └── Research_Paper.md
│
└── .venv/
```

## 10. Expected Project Outputs

The dashboard provides:

- Interactive data exploration.
- Route-level diagnostic summaries.
- Geographic and shipping mode analysis.
- Order-level search.
- Filtered shipment CSV export.
- Data quality report CSV export.

## 11. Conclusion

This project provides a reproducible analytical workflow for exploring the Nassau Candy Distributor dataset.

It combines data preparation, validation, exploratory analysis, interactive visualization, and downloadable reports.

The source-date anomaly is an important limitation. Operational shipping efficiency conclusions require confirmation of the original date fields.

**Project:** Nassau Candy Distributor | Shipping Route Efficiency Analysis

**Platform:** Unified Mentor

**Application:** Python and Streamlit