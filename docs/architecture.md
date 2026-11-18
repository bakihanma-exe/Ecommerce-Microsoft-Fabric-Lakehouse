# Olist Microsoft Fabric Lakehouse architecture

## Source
Brazilian E-Commerce Public Dataset by Olist (Kaggle), nine related CSVs from 2016–2018. See `schemas/olist_schema.json` for exact headers, table grains and keys.

## Flow
Kaggle CSVs → optional ADF copy/orchestration → ADLS Gen2 / Fabric Lakehouse Files landing → Fabric Bronze Delta → Fabric Silver Delta → Fabric Gold Delta → Power BI.

## Bronze
One Delta table per source CSV. Raw columns and values are preserved as strings; ingestion timestamp and source file are added. Full-refresh overwrite is used for repeatable loading of this fixed snapshot.

## Silver
- Cast timestamps, numeric measures and keys to appropriate types.
- Trim string values.
- Deduplicate using actual source grain: order_id; customer_id; (order_id, order_item_id); (order_id, payment_sequential); review_id; product_id; seller_id.
- Geolocation is not unique by zip prefix. Aggregate coordinate samples by zip prefix, city and state before using it as a lookup.
- Keep one-to-many child tables separate.

## Gold
- `gold_olist_order_fact`: one row per order; item, payment and review data are aggregated to order_id before joining.
- Monthly performance, order status, customer state, category, payment type, seller and customer lifetime summaries.
- Currency is BRL. Item value and freight are distinct measures; order value in this project is their sum.

## Fan-out protection
Never join raw order_items × raw payments × raw reviews to orders. The resulting multiplicative rows overstate metrics. Aggregate each child to order grain first, then join.

## Security, licensing and operations
Kaggle credentials are local only. Raw data is not committed. Dataset license is CC BY-NC-SA 4.0; use for non-commercial portfolio/learning and retain attribution. This is a historical static snapshot, not a streaming source; no watermark/CDC is claimed.
