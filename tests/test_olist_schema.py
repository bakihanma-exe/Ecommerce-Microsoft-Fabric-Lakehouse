import csv
import tempfile
import unittest
from pathlib import Path
from scripts.validate_olist_dataset import SCHEMA, validate

class OlistSchemaTests(unittest.TestCase):
    def test_all_expected_headers_pass(self):
        with tempfile.TemporaryDirectory() as d:
            for name, cols in SCHEMA["files"].items():
                with (Path(d)/name).open("w", encoding="utf-8", newline="") as f:
                    w=csv.writer(f); w.writerow(cols); w.writerow([""]*len(cols))
            self.assertEqual([], validate(d))

    def test_missing_files_are_reported(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(9, len(validate(d)))

    def test_wrong_header_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            for name, cols in SCHEMA["files"].items():
                actual=list(cols)
                if name == "olist_orders_dataset.csv": actual[0]="bad_order_id"
                with (Path(d)/name).open("w", encoding="utf-8", newline="") as f:
                    csv.writer(f).writerow(actual)
            errors=validate(d)
            self.assertEqual(1, len(errors))
            self.assertIn("olist_orders_dataset.csv", errors[0])

if __name__ == "__main__":
    unittest.main()
