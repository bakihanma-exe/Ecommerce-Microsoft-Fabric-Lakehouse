# Power BI dashboard design — Olist

Connect Power BI to curated Gold tables in the Fabric Lakehouse SQL analytics endpoint.

## Page 1 — Executive overview
- Distinct order count
- Product revenue (BRL)
- Freight value (BRL)
- Order value (product revenue + freight)
- Average review score
- Monthly order and product revenue trend

## Page 2 — Delivery performance
- Delivered vs cancelled vs other order statuses
- Average delivery days
- Late-delivery rate (only orders with a delivered timestamp and estimated delivery date)
- Delivery delay distribution by customer state

## Page 3 — Product and seller performance
- Product revenue and item count by translated category
- Top categories by product revenue
- Seller item count, distinct orders and product revenue

## Page 4 — Customer and payment insights
- Order count and lifetime order value by customer_unique_id
- Customer state distribution
- Payment value and transaction count by payment type
- Average payment installments

## Model and metric caveats
- Use `gold_olist_order_fact` for order-level measures. Use category/seller tables for their own grains.
- Product revenue = sum(order item price), freight = sum(freight_value), order value = their sum. Currency is BRL.
- These measures are not profit, margin or accounting revenue.
- Payments are a separate financial fact; do not sum payment_value after joining to item rows.
- Delivery delay = actual delivered date minus estimated delivery date; positive means late. Exclude undelivered orders from delivered-late rate.
