# Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

## Abstract

This project presents a data analytics workflow for examining the shipping records of Nassau Candy Distributor. Its primary objective is to analyze order volumes, factory-to-customer state-level route assignments, shipping modes, geographic distribution, and recorded shipping lead times.

The project uses Python, Pandas, NumPy, Plotly, and Streamlit to implement data validation, feature engineering, descriptive analysis, and interactive visualization.

The dataset contains 10,194 records and 18 original columns. A significant source-data anomaly was identified during date validation. Under day-first date parsing, order dates range from 2 January 2024 to 31 December 2025, while ship dates range from 30 June 2026 to 28 June 2030. Calculated lead times range from 904 to 1,642 days, and all 10,194 records exceed the provisional 180-day screening threshold.

Therefore, recorded lead times are treated as unverified diagnostic values rather than confirmed delivery durations. The project preserves the original dates and emphasizes data integrity, transparent reporting, and validation before operational recommendations.

## 1. Introduction

Shipping analysis helps organizations examine order distribution, shipment patterns, and geographic concentration. Route-level analysis provides a structured way to investigate how recorded orders are distributed across assigned factories and customer locations.

This project develops a reproducible analytical workflow using the Nassau Candy Distributor dataset. It combines data preparation, validation, descriptive statistics, interactive charts, and order-level exploration.

A key part of the project is identifying data-quality issues before interpreting operational performance. The source dates contain a significant inconsistency, so the analysis distinguishes recorded values from verified shipping performance.

## 2. Project Objectives

The main objectives are:

1. Calculate lead time using Ship Date minus Order Date.
2. Validate source records, dates, identifiers, and product mappings.
3. Assign factories using the product-to-factory mapping supplied in the project brief.
4. Aggregate records by assigned factory, customer state, region, and shipping mode.
5. Examine unique order volumes and recorded lead-time patterns.
6. Analyze geographic distribution using customer state and region.
7. Develop an interactive Streamlit dashboard with filters and order-level search.
8. Export filtered records and data-quality reports.
9. Document source-data limitations and recommend further validation.

## 3. Dataset Description

The supplied CSV contains 10,194 rows and 18 source columns.

The original fields include:

- Row ID
- Order ID
- Order Date
- Ship Date
- Ship Mode
- Customer ID
- Country/Region
- City
- State/Province
- Postal Code
- Division
- Region
- Product ID
- Product Name
- Sales
- Units
- Gross Profit
- Cost

### 3.1 Initial Data Quality

The initial dataset audit identified:

- Total records: 10,194
- Original source columns: 18
- Missing source values: 0
- Duplicate full rows: 0
- Duplicate Row IDs: 0
- Distinct products: 15
- Unmapped products: 0

Order IDs repeat because multiple product records can belong to the same order. Therefore, repeated Order IDs are not automatically treated as duplicate records.

The source dataset does not contain a factory field or customer latitude and longitude.

## 4. Methodology

### 4.1 Data Loading and Validation

The source CSV is loaded using Pandas.

The pipeline checks:

- Required source columns.
- Missing source values.
- Duplicate Row IDs.
- Duplicate Order IDs.
- Invalid order dates.
- Invalid ship dates.
- Negative lead times.
- Lead times exceeding 180 days.
- Products without an assigned factory.

Postal codes are retained as text to avoid unwanted numeric conversion.

### 4.2 Date Processing and Lead-Time Calculation

Dates are parsed using the day-month-year format.

Lead time is calculated using:

Lead Time Days = Ship Date - Order Date

The difference is measured in calendar days.

The project uses 180 days as a provisional anomaly screening threshold. This is a data-quality rule, not a confirmed contractual shipping SLA.

Original source dates are preserved. No unsupported date corrections are applied.

### 4.3 Factory Assignment and Route Construction

Factory assignments are derived from the product-to-factory mapping supplied in the project brief.

The route is represented as:

Assigned Factory → Customer State

This provides a basis for grouping records by assigned factory and customer state.

Factory assignment is an inferred analytical field, not an original source attribute. The resulting route is a logical grouping, not a verified physical road route.

### 4.4 Descriptive Analysis

The dashboard supports the following analyses:

- Monthly unique order trends.
- Recorded sales by product division.
- Factory-to-state route summaries.
- Unique order volume by route.
- Recorded lead-time averages and variability.
- Customer-state order distribution.
- Shipping mode comparisons.
- Order-level record searches.

Lead-time comparisons remain diagnostic because the source dates have not been validated.

### 4.5 Interactive Dashboard Development

The Streamlit application provides:

- Order date filters.
- Customer region filters.
- Customer state filters.
- Shipping mode filters.
- Anomaly inclusion controls.
- KPI summaries.
- Interactive charts and tables.
- Order-level search.
- Filtered CSV export.
- Data-quality report export.

The dashboard presents warnings wherever source-data limitations affect interpretation.

## 5. Findings and Results

### 5.1 Dataset Overview

The dataset contains 10,194 records and 18 source fields. All 15 distinct products have an assigned factory through the supplied product mapping.

No missing source values, duplicate full rows, or duplicate Row IDs were identified in the initial audit.

### 5.2 Source Date Anomaly

Date validation identified a major temporal inconsistency.

| Metric | Observed result |
|---|---|
| Earliest order date | 2 January 2024 |
| Latest order date | 31 December 2025 |
| Earliest ship date | 30 June 2026 |
| Latest ship date | 28 June 2030 |
| Minimum lead time | 904 days |
| Median lead time | 1,274 days |
| Maximum lead time | 1,642 days |
| Records exceeding 180 days | 10,194 |
| Anomaly percentage | 100% |

All records exceed the provisional 180-day screening threshold.

These values require confirmation from the data owner. The available dataset does not establish whether the ship dates are incorrect, shifted, or associated with another reporting period.

### 5.3 Route Analysis

The project constructs route groups using inferred factory assignments and customer states.

Route summaries include:

- Unique order counts.
- Average recorded lead time.
- Lead-time variability.
- Recorded sales.

The dashboard provides diagnostic route rankings. However, these rankings do not establish actual shipping efficiency because all source records contain anomalous lead times.

### 5.4 Geographic Analysis

Geographic analysis uses customer state and region information.

The dashboard summarizes unique order volumes and recorded commercial values by state.

Customer latitude and longitude are unavailable. Therefore, the analysis does not calculate exact road distances, customer-level routes, or geographic travel times.

### 5.5 Shipping Mode Analysis

The dataset contains multiple shipping modes.

The dashboard compares unique order counts and recorded lead-time summaries across these modes.

Since all records exceed the provisional anomaly threshold, the lead-time differences are not treated as verified shipping service performance.

The analysis is descriptive and does not establish a causal relationship between shipping mode and delivery duration.

### 5.6 Commercial Metrics

The dataset includes Sales, Gross Profit, and Cost.

These fields support commercial summaries and division-level comparisons.

However, the available data does not establish actual transportation or freight expenditure. Therefore, the project does not claim to calculate shipping cost efficiency or cost-versus-time trade-offs.

## 6. Recommendations

Based on the initial findings, the following actions are recommended:

1. Confirm the date format and date-field definitions with the data owner.
2. Verify whether the recorded ship dates belong to the same reporting period as the order dates.
3. Obtain source-system documentation or an updated dataset if date corrections are required.
4. Confirm the business definition of a shipment and the relationship between order IDs and product rows.
5. Obtain customer coordinates or validated geographic reference data for more detailed routing analysis.
6. Confirm the operational definition of delayed delivery and obtain an approved SLA threshold.
7. Obtain actual freight expenditure to support transportation cost analysis.
8. Rerun lead-time comparisons and route rankings after source-date validation.
9. Preserve an audit trail of any approved source-data corrections.

## 7. Limitations

The project has several limitations:

1. Source date inconsistencies prevent reliable measurement of actual delivery duration.
2. The 180-day anomaly threshold is provisional and is not a contractual SLA.
3. Factory assignments are inferred from the supplied product mapping.
4. Customer coordinates are unavailable.
5. Geographic analysis is limited to state and region summaries.
6. Exact road distances and physical route optimization are not calculated.
7. Sales and gross profit are not transportation expenses.
8. No validated freight-cost data is available.
9. Shipping mode comparisons are descriptive rather than causal.

These limitations are explicitly communicated in the dashboard and supporting documentation.

## 8. Conclusion

This project establishes a reproducible data preparation and analytical workflow for exploring the Nassau Candy Distributor dataset.

It combines Python-based data processing, data-quality validation, descriptive analysis, interactive visualization, and downloadable reports.

The most important initial finding is the source-date anomaly affecting all 10,194 records. This prevents the project from making reliable claims about actual shipping duration or operational route efficiency.

By preserving the original data, reporting anomalies transparently, and documenting analytical limitations, the project provides a responsible foundation for further shipping analysis.

Once the data owner confirms the date fields and supplies any required corrections, the same analytical pipeline and dashboard can support more reliable route, regional, and shipping mode comparisons.

## 9. Technology Stack

| Technology | Application |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data manipulation and aggregation |
| NumPy | Numerical operations |
| Plotly | Interactive visualizations |
| Streamlit | Dashboard development |
| Unittest | Automated pipeline testing |
| CSV | Source data and report exports |

## 10. Project Deliverables

The project includes:

- Reproducible Python data pipeline.
- Interactive Streamlit dashboard.
- Source dataset.
- Data dictionary.
- Automated pipeline tests.
- Executive summary.
- Research paper.
- Downloadable filtered shipment records.
- Downloadable data-quality report.

**Project Title:** Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

**Platform:** Unified Mentor

**Application:** Python and Streamlit