# Olist dataset setup

Dataset: Brazilian E-Commerce Public Dataset by Olist
Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
License: CC BY-NC-SA 4.0 (Attribution-NonCommercial-ShareAlike). Use for non-commercial learning/portfolio demonstration, attribute Olist, and review the license before redistribution or derivative sharing.

## Download
From the repository root run:
```bash
bash scripts/download_olist_dataset.sh
python scripts/validate_olist_dataset.py
```
The Kaggle CLI uses your own local credentials. Never commit the Kaggle token.

The nine CSV files are extracted into `data/raw/`. Upload them to your Fabric Lakehouse Files area at `Files/landing/olist/`.

## Files
See `schemas/olist_schema.json` for exact header lists, grains and keys. Raw data is intentionally excluded from Git because of dataset licensing and size.
