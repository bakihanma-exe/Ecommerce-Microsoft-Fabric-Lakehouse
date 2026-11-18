# E-Commerce Microsoft Fabric Lakehouse — Olist

An end-to-end portfolio project using the **Brazilian E-Commerce Public Dataset by Olist** and a Microsoft Fabric medallion architecture.

## Dataset
- Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- License: CC BY-NC-SA 4.0 — attribution required; non-commercial use only; share-alike applies to adapted dataset material.
- Period: 2016–2018
- Nine relational CSV files: orders, customers, order items, payments, reviews, products, sellers, geolocation and category translations.
- Exact headers and table grain: `schemas/olist_schema.json`.

Raw data is not committed. Download with your own Kaggle CLI credentials using `bash scripts/download_olist_dataset.sh`, then validate with `python scripts/validate_olist_dataset.py`. Never commit Kaggle tokens or raw customer data.

## Architecture
Kaggle Olist CSVs → ADF (optional orchestration/copy to ADLS Gen2) → Fabric Lakehouse Files landing → Bronze Delta → Silver Delta → Gold Delta → Power BI.

## Repository
- `schemas/olist_schema.json`: nine-file source contract and grains
- `scripts/download_olist_dataset.sh`: official Kaggle CLI download
- `scripts/validate_olist_dataset.py`: exact file/header validation
- `tests/test_olist_schema.py`: standard-library validator tests
- `notebooks/00_source_schema_discovery.py`: profile raw files
- `notebooks/01_bronze_ingestion.py`: one Bronze Delta table per source file
- `notebooks/02_silver_transformation.py`: typed, deduplicated Silver tables
- `notebooks/03_gold_aggregation.py`: order fact and business aggregates
- `sql/data_quality_checks.sql`: key, value, referential and date checks
- `docs/olist-dataset-guide.md`: setup, grain, join and KPI decisions
- `docs/architecture.md`: layer design and orchestration

## Run
1. Install/configure Kaggle CLI locally.
2. Run `bash scripts/download_olist_dataset.sh`.
3. Run `python scripts/validate_olist_dataset.py`.
4. Upload the nine CSVs to Fabric Lakehouse `Files/landing/olist/`.
5. Run notebooks 00, 01, 02, 03 in order.
6. Run the SQL checks against the created Silver/Gold tables.
7. Connect Power BI to the Gold tables via the Fabric Lakehouse SQL analytics endpoint.

## Important modelling choices
The item, payment and review tables are one-to-many from orders. The Gold order fact aggregates each child table to one row per order before joining. This prevents join fan-out and overstated totals. Revenue values are item price plus freight in BRL, not accounting revenue, profit or margin.

The dataset is a static historical snapshot. The notebooks use full refresh/overwrite; this is not incremental CDC. Fabric notebooks must be run in a configured workspace before claiming end-to-end execution.
