-- Microsoft Fabric SQL analytics endpoint / Spark SQL checks.
-- Run after the Silver and Gold notebooks create these tables.

-- Primary key uniqueness: orders.
SELECT order_id, COUNT(*) AS duplicate_count
FROM silver_olist_orders GROUP BY order_id HAVING COUNT(*) > 1;

-- Composite business keys: order items and payments.
SELECT order_id, order_item_id, COUNT(*) AS duplicate_count
FROM silver_olist_order_items GROUP BY order_id, order_item_id HAVING COUNT(*) > 1;

SELECT order_id, payment_sequential, COUNT(*) AS duplicate_count
FROM silver_olist_order_payments GROUP BY order_id, payment_sequential HAVING COUNT(*) > 1;

-- Required identifiers and valid measures.
SELECT COUNT(*) AS invalid_order_ids FROM silver_olist_orders WHERE order_id IS NULL;
SELECT COUNT(*) AS invalid_item_values FROM silver_olist_order_items WHERE order_id IS NULL OR price < 0 OR freight_value < 0;
SELECT COUNT(*) AS invalid_payment_values FROM silver_olist_order_payments WHERE order_id IS NULL OR payment_value < 0;
SELECT COUNT(*) AS invalid_review_scores FROM silver_olist_order_reviews
WHERE review_score IS NOT NULL AND (review_score < 1 OR review_score > 5);

-- Referential integrity.
SELECT COUNT(*) AS orphan_item_orders
FROM silver_olist_order_items i LEFT ANTI JOIN silver_olist_orders o ON i.order_id = o.order_id;

SELECT COUNT(*) AS orphan_products
FROM silver_olist_order_items i LEFT ANTI JOIN silver_olist_products p ON i.product_id = p.product_id;

-- Timestamp consistency.
SELECT COUNT(*) AS delivered_before_purchase
FROM silver_olist_orders
WHERE order_delivered_customer_date < order_purchase_timestamp;

-- Gold fact grain: one row per order.
SELECT COUNT(*) AS fact_rows, COUNT(DISTINCT order_id) AS distinct_orders
FROM gold_olist_order_fact;
