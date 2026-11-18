# Olist Fabric Lakehouse — interview preparation

## Project walkthrough
"I used the Brazilian E-Commerce Public Dataset by Olist, which contains nine related CSVs for orders, customers, order items, payments, reviews, products, sellers, geolocation and category translation. I designed a Fabric medallion pipeline: Bronze preserves source data, Silver standardizes types and enforces table grain, and Gold produces order-level and business aggregates."

Only describe cloud steps you have personally executed. This repository provides implementation code; it does not itself prove a Fabric workspace deployment.

## Key engineering decisions
- Bronze reads source CSV fields as strings to avoid unreliable schema inference.
- Silver casts order timestamps, item prices, freight, payment values, review scores and keys.
- Deduplication uses each table's true key/grain. Order items use (order_id, order_item_id); payments use (order_id, payment_sequential).
- Geolocation has many coordinate samples per zip prefix, so Silver aggregates them before dimension use.
- Items, payments and reviews are aggregated to order_id before joining to orders. This prevents one-to-many join fan-out and inflated revenue.
- Gold revenue is item price + freight in BRL. It is not profit or accounting revenue because product cost, discounts and all accounting adjustments are not supplied.
- The dataset is a fixed historical snapshot; the implemented load is full refresh, not CDC.

## Interview questions to prepare
1. Why preserve raw values as strings in Bronze?
2. How did you decide the grain and deduplication key for each table?
3. What is join fan-out? Demonstrate it with orders, items and payments.
4. Why is customer_id different from customer_unique_id?
5. Why does geolocation need aggregation before joining?
6. How would you implement incremental ingestion if a future source provided a reliable modified timestamp?
7. How would you quarantine invalid rows and reconcile source/Silver counts?
8. How would you expose Gold tables to Power BI and monitor Fabric pipeline runs?

## Dataset attribution
Olist, Brazilian E-Commerce Public Dataset by Olist, Kaggle. License: CC BY-NC-SA 4.0 (non-commercial).
