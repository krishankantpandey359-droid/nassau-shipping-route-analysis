# Nassau Candy Distributor
## Factory-to-Customer Shipping Route Efficiency Analysis

An interactive Streamlit dashboard and reproducible Python data pipeline developed for the Unified Mentor Data Analytics Project.

This project analyzes order records, factory-to-customer route assignments, shipping modes, geographic distribution, recorded lead times, and source-data quality.

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

Follow these steps to run the dashboard locally.

1. Open the existing `Nassau_Shipping_Route_Analysis` folder in VS Code.
2. Open Terminal → New Terminal.
3. Run:

```powershell
.\RUN_PROJECT.bat
```

4. Wait for the application to start.
5. Open the local URL displayed by Streamlit, usually:

```text
http://localhost:8501
```

Keep the terminal open while using the dashboard.

Press `Ctrl + C` to stop the application.

### Requirements

- Python 3.10 or newer.
- Internet connection for initial dependency installation.
- VS Code or another Python-compatible editor.

The launcher creates and reuses the project's local `.venv` environment.

## 3. Install Dependencies Manually

If you want to install dependencies manually, run:

```powershell
python -m pip install -r requirements.txt
```

Start the dashboard:

```powershell
python -m streamlit run app.py
```

## 4. Automated Quality Checks

Run the automated pipeline tests:

```powershell
python -m unittest discover -s tests -v
```

The current test suite contains 11 automated tests covering:

1. Product-to-factory mapping.
2. Date anomaly preservation.
3. Expected dataset size.
4. Lead-time calculation.
5. Unique Row IDs.
6. Duplicate full-row validation.
7. Factory coordinate availability.
8. Route generation.
9. Missing required column validation.
10. Date anomaly edge cases.
11. Required source column validation.

### Latest Test Results

- Total tests: 11
- Passed: 11
- Failed: 0
- Errors: 0
- Final status: OK

All 11 automated tests passed during the latest recorded validation.

## 5. Dashboard Features

The Streamlit dashboard contains six main sections.

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

Factory assignments are inferred from the supplied product-to-factory mapping.

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
- Downloadable CSV report exports.

## 6. Important Source-Data Findings

The supplied dataset contains:

| Metric | Finding |
|---|---:|
| Total records | 10,194 |
| Source columns | 18 |
| Distinct products | 15 |
| Missing source values | 0 |
| Duplicate full rows | 0 |
| Duplicate Row IDs | 0 |
| Duplicate Order IDs | 1,645 |
| Unmapped products | 0 |

Duplicate Order IDs represent multiple product records associated with an order and are not automatically treated as duplicate rows.

### Recorded Date Ranges

| Date Field | Recorded Range |
|---|---|
| Order Date | 2 January 2024 to 31 December 2025 |
| Ship Date | 30 June 2026 to 28 June 2030 |
| Lead Time | 904 to 1,642 days |

The median recorded lead time is 1,274 days.

All 10,194 records exceed the provisional 180-day lead-time screening threshold.

### Data Integrity Notice

The source dates are preserved. The pipeline does not silently modify or fabricate date corrections.

The 180-day threshold is a provisional screening rule, not a contractual delivery SLA.

Route rankings and shipping-mode lead-time comparisons are diagnostic only. They must not be interpreted as verified operational shipping performance until the data owner confirms or corrects the source date fields.

## 7. Project Scope and Limitations

The project has the following limitations:

- Factory assignments are inferred from the supplied product-to-factory mapping.
- Factory assignments are derived fields, not original CSV columns.
- Customer latitude and longitude are unavailable.
- Geographic analysis is limited to customer-state summaries.
- Exact road distances and route optimization are not calculated.
- Sales and gross profit are commercial measures, not freight costs.
- Actual transportation expenses are unavailable.
- Shipping mode comparisons are descriptive, not causal.
- Recorded lead times remain unverified because of the source-date anomaly.

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
└── reports/
    ├── Executive_Summary.md
    └── Research_Paper.md
```

The local `.venv/` and `__pycache__/` directories are excluded from version control through `.gitignore`.

## 10. Expected Project Outputs

The dashboard provides:

- Interactive data exploration.
- Route-level diagnostic summaries.
- Geographic and shipping mode analysis.
- Order-level search.
- Filtered shipment CSV export.
- Data quality report CSV export.

## 11. Repository

GitHub Repository:

https://github.com/krishankantpandey359-droid/nassau-shipping-route-analysis

The repository contains the project source code, dataset, documentation, reports, and automated tests.

## 12. Conclusion

This project provides a reproducible analytical workflow for exploring the Nassau Candy Distributor dataset.

It combines data preparation, validation, exploratory analysis, interactive visualization, and downloadable reports.

The source-date anomaly is an important limitation. Operational shipping efficiency conclusions require confirmation of the original date fields.

### Project Information

- Project: Nassau Candy Distributor
- Analysis: Factory-to-Customer Shipping Route Efficiency
- Platform: Unified Mentor
- Application: Python and Streamlit
- Repository: GitHub
