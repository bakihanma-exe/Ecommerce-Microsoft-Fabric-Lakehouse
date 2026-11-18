#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/data/raw"
mkdir -p "$OUT"
python -m pip install --upgrade kaggle
kaggle datasets download -d olistbr/brazilian-ecommerce -p "$OUT" --unzip
echo "Olist CSVs extracted to $OUT"
echo "Run: python scripts/validate_olist_dataset.py"
