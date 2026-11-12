
import unittest
from pathlib import Path
import sys
import tempfile

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pipeline import (
    load_data,
    PRODUCT_FACTORY,
    FACTORY_COORDS,
    REQUIRED_COLUMNS,
    ANOMALY_THRESHOLD_DAYS,
)


class PipelineTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df, cls.audit = load_data(
            ROOT / "data" / "Nassau_Candy_Distributor.csv"
        )

    def test_expected_dataset_size(self):
        self.assertEqual(len(self.df), 10194)

    def test_required_source_columns(self):
        for column in REQUIRED_COLUMNS:
            self.assertIn(column, self.df.columns)

    def test_all_products_are_mapped(self):
        self.assertEqual(self.audit["unmapped_products"], 0)

        self.assertTrue(
            set(self.df["Factory"].dropna()).issubset(
                FACTORY_COORDS
            )
        )

        self.assertEqual(
            self.df["Product Name"].nunique(),
            len(PRODUCT_FACTORY)
        )

    def test_lead_time_calculation_for_all_rows(self):
        expected = (
            self.df["Ship Date"] - self.df["Order Date"]
        ).dt.days

        pd.testing.assert_series_equal(
            self.df["Lead Time Days"],
            expected,
            check_names=False
        )

    def test_date_anomaly_is_visible_not_corrected(self):
        self.assertEqual(
            self.audit["over_180_day_lead_times"],
            10194
        )

        self.assertTrue(
            self.df["Date anomaly"].all()
        )

    def test_unique_row_ids(self):
        self.assertEqual(
            self.audit["duplicate_row_ids"],
            0
        )

    def test_no_duplicate_full_rows(self):
        self.assertEqual(
            self.audit["duplicate_full_rows"],
            0
        )

    def test_factory_coordinates_are_available(self):
        mapped = self.df["Factory"].notna()

        self.assertTrue(
            self.df.loc[mapped, "Factory Latitude"].notna().all()
        )

        self.assertTrue(
            self.df.loc[mapped, "Factory Longitude"].notna().all()
        )

    def test_route_generation(self):
        self.assertTrue(
            self.df["Route"].notna().all()
        )

        self.assertTrue(
            self.df["Route"].str.contains(" to ").all()
        )

    def test_date_anomaly_edge_cases(self):
        rows = []

        test_dates = [
            ("01-01-2025", "11-01-2025"),
            ("", "11-01-2025"),
            ("11-01-2025", "10-01-2025"),
            ("01-01-2025", "02-01-2025"),
            ("01-01-2025", "02-07-2025"),
        ]

        for index, (order_date, ship_date) in enumerate(test_dates):
            row = {column: "Test" for column in REQUIRED_COLUMNS}

            row.update({
                "Row ID": index + 1,
                "Order ID": f"TEST-{index + 1}",
                "Order Date": order_date,
                "Ship Date": ship_date,
                "Product Name": "Nerds",
                "State/Province": "California",
                "Postal Code": "00123",
                "Sales": 100,
                "Units": 2,
                "Gross Profit": 20,
                "Cost": 80,
            })

            rows.append(row)

        test_df = pd.DataFrame(rows)

        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "test_data.csv"
            test_df.to_csv(csv_path, index=False)

            result, audit = load_data(csv_path)

        expected_anomalies = [False, True, True, False, True]

        self.assertEqual(
            result["Date anomaly"].tolist(),
            expected_anomalies
        )

        self.assertEqual(
            result["Lead Time Days"].iloc[0],
            10
        )

        self.assertTrue(
            pd.isna(result["Lead Time Days"].iloc[1])
        )

        self.assertEqual(
            result["Lead Time Days"].iloc[2],
            -1
        )

        self.assertEqual(
            result["Lead Time Days"].iloc[3],
            1
        )

        self.assertEqual(
            result["Lead Time Days"].iloc[4],
            182
        )

    def test_missing_required_column_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "invalid_data.csv"

            pd.DataFrame({
                "Row ID": [1]
            }).to_csv(csv_path, index=False)

            with self.assertRaises(ValueError):
                load_data(csv_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
