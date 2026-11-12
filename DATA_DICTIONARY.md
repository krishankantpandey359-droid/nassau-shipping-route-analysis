# Data Dictionary

This document describes the original dataset fields and the additional fields derived during the analysis pipeline.

## 1. Original Source Columns

| Field | Description |
|---|---|
| Row ID | Unique row identifier |
| Order ID | Order identifier; can repeat across multiple product rows |
| Order Date | Date on which the order was placed |
| Ship Date | Recorded shipment date |
| Ship Mode | Shipping method |
| Customer ID | Customer identifier |
| Country/Region | Customer country or region |
| City | Customer city |
| State/Province | Customer state or province |
| Postal Code | Postal or ZIP code, stored as text |
| Division | Product division |
| Region | Customer region |
| Product ID | Product identifier |
| Product Name | Product name |
| Sales | Recorded sales value |
| Units | Number of units |
| Gross Profit | Recorded gross profit |
| Cost | Recorded cost value |

## 2. Derived Analysis Columns

| Field | Description |
|---|---|
| Lead Time Days | Calculated as Ship Date minus Order Date, measured in days |
| Factory | Factory assigned using the product-to-factory mapping supplied in the project brief |
| Route | Derived route from the assigned factory to the customer's state |
| Date Anomaly | Flags records with missing dates, negative lead times, or lead times exceeding the provisional 180-day screening threshold |

## 3. Data Interpretation Notes

- The original dataset contains 18 source columns.
- The analysis pipeline adds derived columns for shipment analysis.
- Factory is inferred from the supplied product mapping. It is not an original source field.
- Customer latitude and longitude are not available in the source dataset.
- Duplicate Order IDs are not automatically treated as errors because an order can contain multiple product rows.
- The 180-day threshold is a provisional data-quality screening rule, not a confirmed contractual delivery SLA.
- All 10,194 records exceed this provisional threshold in the supplied dataset.
- Original source dates are preserved. The pipeline does not silently correct date values.