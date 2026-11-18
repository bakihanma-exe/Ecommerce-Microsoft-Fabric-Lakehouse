# Microsoft Fabric notebook — Olist Silver -> Gold
# Aggregate one-to-many child tables to order grain before joining.
from pyspark.sql import functions as F

orders = spark.table("silver_olist_orders")
customers = spark.table("silver_olist_customers")
items = spark.table("silver_olist_order_items")
payments = spark.table("silver_olist_order_payments")
reviews = spark.table("silver_olist_order_reviews")
products = spark.table("silver_olist_products")
sellers = spark.table("silver_olist_sellers")
translations = spark.table("silver_olist_category_translation")

def save_gold(df, name):
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_olist_" + name)
    print(f"gold_olist_{name}: {df.count()} rows")

item_order = items.groupBy("order_id").agg(
    F.count("*").alias("item_count"), F.sum("price").alias("product_revenue_brl"),
    F.sum("freight_value").alias("freight_revenue_brl"),
    F.countDistinct("seller_id").alias("seller_count"),
    F.countDistinct("product_id").alias("distinct_product_count"))
payment_order = payments.groupBy("order_id").agg(
    F.sum("payment_value").alias("payment_total_brl"), F.count("*").alias("payment_count"),
    F.max("payment_installments").alias("max_payment_installments"))
review_order = reviews.groupBy("order_id").agg(
    F.avg("review_score").alias("average_review_score"), F.count("*").alias("review_count"))

order_fact = (orders.join(item_order, "order_id", "left")
    .join(payment_order, "order_id", "left").join(review_order, "order_id", "left")
    .join(customers.select("customer_id","customer_unique_id","customer_city","customer_state"), "customer_id", "left")
    .withColumn("purchase_date", F.to_date("order_purchase_timestamp"))
    .withColumn("delivery_days", F.when(F.col("order_delivered_customer_date").isNotNull(),
        F.datediff(F.to_date("order_delivered_customer_date"), F.to_date("order_purchase_timestamp"))))
    .withColumn("delivery_delay_days", F.when(F.col("order_delivered_customer_date").isNotNull(),
        F.datediff(F.to_date("order_delivered_customer_date"), F.to_date("order_estimated_delivery_date"))))
    .withColumn("is_delivered_late", F.col("delivery_delay_days") > 0)
    .withColumn("order_value_brl", F.coalesce("product_revenue_brl", F.lit(0.0)) + F.coalesce("freight_revenue_brl", F.lit(0.0))))
save_gold(order_fact, "order_fact")

monthly = order_fact.groupBy(F.date_trunc("month","order_purchase_timestamp").cast("date").alias("purchase_month")).agg(
    F.countDistinct("order_id").alias("order_count"), F.sum("product_revenue_brl").alias("product_revenue_brl"),
    F.sum("freight_revenue_brl").alias("freight_revenue_brl"), F.avg("average_review_score").alias("average_review_score"))
save_gold(monthly, "monthly_performance")

status = order_fact.groupBy("order_status").agg(F.countDistinct("order_id").alias("order_count"), F.sum("order_value_brl").alias("order_value_brl"))
save_gold(status, "order_status_summary")

state = order_fact.groupBy("customer_state").agg(F.countDistinct("order_id").alias("order_count"),
    F.sum("order_value_brl").alias("order_value_brl"), F.avg("average_review_score").alias("average_review_score"))
save_gold(state, "customer_state_summary")

category_items = items.join(products.select("product_id","product_category_name"), "product_id", "left").join(translations, "product_category_name", "left")
category_items = category_items.withColumn("category", F.coalesce("product_category_name_english","product_category_name"))
category = category_items.groupBy("category").agg(F.count("*").alias("item_count"),
    F.sum("price").alias("product_revenue_brl"), F.sum("freight_value").alias("freight_revenue_brl"))
save_gold(category, "category_performance")

payment_type = payments.groupBy("payment_type").agg(F.count("*").alias("payment_transaction_count"),
    F.sum("payment_value").alias("payment_value_brl"), F.avg("payment_installments").alias("average_installments"))
save_gold(payment_type, "payment_type_summary")

seller = items.groupBy("seller_id").agg(F.count("*").alias("item_count"),
    F.countDistinct("order_id").alias("order_count"), F.sum("price").alias("product_revenue_brl"),
    F.sum("freight_value").alias("freight_revenue_brl")).join(sellers, "seller_id", "left")
save_gold(seller, "seller_performance")

customer = order_fact.groupBy("customer_unique_id","customer_state").agg(
    F.countDistinct("order_id").alias("order_count"), F.sum("order_value_brl").alias("lifetime_order_value_brl"),
    F.max("purchase_date").alias("most_recent_order_date"))
save_gold(customer, "customer_lifetime_summary")
