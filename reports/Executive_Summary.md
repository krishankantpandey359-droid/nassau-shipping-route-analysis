# Executive Summary: Nassau Candy Distributor Shipping Route Analysis

## 1. Project Purpose

The purpose of this project is to develop a reproducible analytical workflow for examining shipment records from Nassau Candy Distributor.

The project focuses on order volume, recorded lead times, factory-to-customer-state route summaries, shipping modes, geographic distribution, and data quality.

An interactive Streamlit dashboard provides data exploration, visual summaries, filters, and downloadable reports.

## 2. Dataset Overview

The supplied dataset contains:

- 10,194 records.
- 18 original source columns.
- 15 distinct products.
- All distinct products mapped to a factory using the supplied project brief.
- Zero missing source values.
- Zero duplicate full rows.
- Zero duplicate Row IDs.

Duplicate Order IDs occur because an order can contain multiple product rows.

The original dataset does not contain a factory field or customer latitude and longitude. Factory assignments are derived from the supplied product mapping.

## 3. Critical Data-Quality Finding

Date validation using the day-month-year format identified a significant temporal inconsistency.

| Metric | Observed result |
|---|---|
| Earliest order date | 2 January 2024 |
| Latest order date | 31 December 2025 |
| Earliest ship date | 30 June 2026 |
| Latest ship date | 28 June 2030 |
| Minimum recorded lead time | 904 days |
| Median recorded lead time | 1,274 days |
| Maximum recorded lead time | 1,642 days |
| Records exceeding 180 days | 10,194 |
| Anomaly percentage | 100% |

All records exceed the provisional 180-day anomaly screening threshold.

The threshold is a data-quality screening rule, not a contractual shipping SLA.

This inconsistency prevents reliable conclusions about actual shipping efficiency. The original dates are preserved, and lead-time and route rankings are presented as diagnostics rather than verified operational performance.

## 4. Dashboard Capabilities

The interactive dashboard includes:

- Overview of filtered records, unique orders, recorded lead time, and recorded sales.
- Monthly unique order trends.
- Recorded sales distribution by division.
- Factory-to-customer-state route aggregation.
- Route-level order volume and lead-time diagnostics.
- State-level geographic summaries.
- Shipping mode comparisons.
- Order-level search and drill-down.
- Data-quality validation.
- Filtered shipment CSV export.
- Data-quality report CSV export.

## 5. Key Limitations

1. Source date fields require confirmation from the data owner.
2. Factory assignments are inferred rather than supplied as original source fields.
3. Customer coordinates are unavailable.
4. Exact road distances and physical route optimization are not calculated.
5. Sales and gross profit are not transportation costs.
6. Actual freight expenditure is unavailable.
7. Shipping mode comparisons are descriptive, not causal.

## 6. Recommendations

1. Request confirmation of the order-date and ship-date fields from the dataset owner.
2. Verify whether the recorded years or date definitions require correction.
3. Obtain an approved operational delivery threshold before calculating delay rates.
4. Add customer coordinates or validated geographic reference data for detailed routing analysis.
5. Obtain actual freight costs to evaluate transportation cost efficiency.
6. Rerun route rankings and shipping mode comparisons after source-date validation.
7. Preserve an audit trail for all approved data corrections.

## 7. Project Outcome

The project delivers a reproducible Python data pipeline, an interactive Streamlit dashboard, automated validation tests, and supporting analytical documentation.

Its primary initial finding is the date inconsistency affecting all 10,194 records.

The project establishes a transparent foundation for further shipping analysis while clearly identifying the source-data validation required before operational conclusions can be made.

**Project:** Nassau Candy Distributor | Shipping Route Efficiency Analysis

**Platform:** Unified Mentor

**Technology:** Python, Pandas, NumPy, Plotly, Streamlit, and Unittest