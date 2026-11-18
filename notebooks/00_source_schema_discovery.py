# Microsoft Fabric notebook — Olist source schema discovery
from pyspark.sql import functions as F

SOURCE_DIR = "Files/landing/olist"
FILES = [
    "olist_orders_dataset.csv", "olist_customers_dataset.csv",
    "olist_order_items_dataset.csv", "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv", "olist_products_dataset.csv",
    "olist_sellers_dataset.csv", "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv"
]

for file_name in FILES:
    path = f"{SOURCE_DIR}/{file_name}"
    df = (spark.read.option("header", True).option("inferSchema", False)
          .option("mode", "PERMISSIVE").csv(path))
    if not df.columns:
        raise ValueError(f"No header discovered for {path}")
    print(f"\n{file_name}: {df.count()} rows")
    for field in df.schema.fields:
        print(f"  {field.name}: {field.dataType.simpleString()}")
    display(df.limit(5))

# Compare the discovered headers with schemas/olist_schema.json before processing.
