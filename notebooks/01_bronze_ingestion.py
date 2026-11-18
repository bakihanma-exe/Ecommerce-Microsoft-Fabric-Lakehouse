# Microsoft Fabric notebook — Olist Bronze ingestion
from pyspark.sql import functions as F

SOURCE_DIR = "Files/landing/olist"
FILES = {
    "olist_orders_dataset.csv": "bronze_olist_orders",
    "olist_customers_dataset.csv": "bronze_olist_customers",
    "olist_order_items_dataset.csv": "bronze_olist_order_items",
    "olist_order_payments_dataset.csv": "bronze_olist_order_payments",
    "olist_order_reviews_dataset.csv": "bronze_olist_order_reviews",
    "olist_products_dataset.csv": "bronze_olist_products",
    "olist_sellers_dataset.csv": "bronze_olist_sellers",
    "olist_geolocation_dataset.csv": "bronze_olist_geolocation",
    "product_category_name_translation.csv": "bronze_olist_category_translation",
}
for file_name, table_name in FILES.items():
    path = f"{SOURCE_DIR}/{file_name}"
    df = (spark.read.option("header", True).option("inferSchema", False)
          .option("mode", "FAILFAST").csv(path))
    if not df.columns:
        raise ValueError(f"CSV has no header: {path}")
    loaded = df.withColumn("_source_file", F.input_file_name()).withColumn("_ingested_at_utc", F.current_timestamp())
    (loaded.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(table_name))
    print(f"{table_name}: {loaded.count()} rows")

# Full-refresh overwrite is intentional for this static historical Kaggle snapshot.
# This is not incremental CDC. Raw source values remain strings in Bronze.
