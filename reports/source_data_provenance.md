# Dataset provenance and source validation

## Exact-file match

The repository file `data/Nassau_Candy_Distributor.csv` was compared with the file named `Nassau Candy Distributor.csv` in the public repository:

- Public copy: https://github.com/aditya72-asg/Nassau-Candy-Data-Analysis
- Public CSV path: `Nassau Candy Distributor.csv`
- Public Git blob SHA: `07cd816c1a715af6a5bc9ba84a24cd33756922e9`
- This repository's CSV Git blob SHA: `07cd816c1a715af6a5bc9ba84a24cd33756922e9`
- File size in the public repository: 1,969,400 bytes
- Data rows: 10,194

The identical Git blob SHA establishes that both repositories contain byte-identical CSV content. The matching file begins with the same 18 columns and the same recorded dates.

## What the match does not establish

The public repository's README describes the file as a Nassau Candy Distributor dataset, but it does not cite a primary data publisher, original download URL, licence, or source-system export. A second copy of the same file is not independent evidence that the dates are correct.

Therefore this match establishes a public mirror/copy, not authoritative data provenance or date validation. It does not justify changing source dates.

## Date anomaly still requiring source-owner confirmation

The source file records:

- Order Date: 2 January 2024 to 31 December 2025.
- Ship Date: 30 June 2026 to 28 June 2030.
- Calculated lead time: 904 to 1,642 days.
- Median calculated lead time: 1,274 days.
- Rows above the provisional 180-day screening threshold: 10,194 of 10,194.

The source dates remain unchanged in the repository. The 180-day value is a screening threshold, not a contractual delivery SLA.

Before correcting dates or drawing shipping-efficiency conclusions, obtain at least one of the following from the dataset owner: the original system export, a source download page with version details, a documented date-format/timezone rule, or a correction notice. Do not subtract a fixed number of days or replace years based on visual plausibility.

## Reuse and licence

The mirrored GitHub repository does not provide a clear licence for the CSV in its README. Public visibility alone does not establish permission to redistribute. Confirm the original dataset licence before reusing or republishing the CSV outside this project.

## Reproducibility references

- This repository's CSV: `data/Nassau_Candy_Distributor.csv`
- Data processing: `src/pipeline.py`
- Data dictionary: `DATA_DICTIONARY.md`
- Automated anomaly tests: `tests/test_pipeline.py`
