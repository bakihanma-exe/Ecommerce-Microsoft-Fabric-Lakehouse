"""Validate the nine original Olist CSV files and their published headers."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
SCHEMA = json.loads((ROOT / "schemas" / "olist_schema.json").read_text(encoding="utf-8"))

def validate(data_dir=DATA_DIR):
    errors = []
    for filename, expected in SCHEMA["files"].items():
        path = Path(data_dir) / filename
        if not path.is_file():
            errors.append(f"Missing file: {filename}")
            continue
        if path.stat().st_size == 0:
            errors.append(f"Empty file: {filename}")
            continue
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            actual = next(csv.reader(f), [])
        if actual != expected:
            errors.append(f"Header mismatch: {filename}; missing={sorted(set(expected)-set(actual))}; extra={sorted(set(actual)-set(expected))}; order_match={actual == expected}")
    return errors

if __name__ == "__main__":
    issues = validate()
    if issues:
        print("\n".join("ERROR: " + x for x in issues))
        raise SystemExit(1)
    print("Olist validation passed: all nine files and headers match.")
