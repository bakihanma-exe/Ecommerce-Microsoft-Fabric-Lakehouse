# Olist dataset guide and model design

## Source and license
Brazilian E-Commerce Public Dataset by Olist: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
License: CC BY-NC-SA 4.0. Attribute Olist. The NonCommercial condition means this dataset is for learning/portfolio demonstration, not commercial redistribution or use. Raw CSVs are deliberately excluded from Git.

## Download and validate
1. Install/configure Kaggle CLI locally (never commit or share your Kaggle token).
2. Run `bash scripts/download_olist_dataset.sh`.
3. Run `python scripts/validate_olist_dataset.py`.
4. Upload the nine CSVs from `data/raw/` to the Fabric Lakehouse Files area at `Files/landing/olist/`.

Exact expected headers are recorded in `schemas/olist_schema.json`. Data dictionary, grain and relationship notes are recorded in this folder.

## Source tables and grains
- Orders: one row per order, key `order_id`.
- Customers: one row per order-specific customer ID; `customer_unique_id` identifies a repeat buyer.
- Order items: one row per line, key `order_id + order_item_id`.
- Payments: one row per payment sequence, key `order_id + payment_sequential`.
- Reviews: review ID grain; multiple reviews may be associated with an order.
- Products: one row per product ID.
- Sellers: one row per seller ID.
- Geolocation: many coordinate samples per zip prefix; Silver aggregates to zip/city/state.
- Category translation: one row per Portuguese category.

## Fabric notebook order
1. `00_source_schema_discovery.py` (optional profile/sample check)
2. `01_bronze_ingestion.py` (raw CSVs to separate Bronze Delta tables)
3. `02_silver_transformation.py` (trim, type, deduplicate by true keys, aggregate geolocation)
4. `03_gold_aggregation.py` (order fact and reporting aggregates)
5. Run `sql/data_quality_checks.sql`.

## Important modelling rule
Do not join raw order items, payments and reviews directly to orders. They are one-to-many child tables. Aggregate each to one row per order before joining to create `gold_olist_order_fact`; this prevents row multiplication and overstated revenue/payment totals.

Gold revenue metrics are based on item price and freight from order items, in BRL. They are not accounting revenue, profit or margin. Product cost is not included. Delivery delay is actual delivered date minus estimated delivery date; positive means late. Cancelled/undelivered orders have null delivery duration.

## Incremental loading
The Kaggle data is a fixed historical snapshot. The notebooks use full refresh/overwrite for reproducibility. Do not claim CDC or watermark-based incremental ingestion for this source.
