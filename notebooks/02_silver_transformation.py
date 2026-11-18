# Microsoft Fabric notebook — Olist Bronze -> Silver
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import IntegerType, DoubleType

def read_bronze(name):
    return spark.table("bronze_olist_" + name)

def trim_strings(df):
    for field in df.schema.fields:
        if field.dataType.simpleString() == "string":
            df = df.withColumn(field.name, F.trim(F.col(field.name)))
    return df

def deduplicate(df, keys):
    w = Window.partitionBy(*keys).orderBy(F.col("_ingested_at_utc").desc_nulls_last())
    return df.withColumn("_rn", F.row_number().over(w)).filter(F.col("_rn") == 1).drop("_rn")

def save(df, name):
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_olist_" + name)
    print(f"silver_olist_{name}: {df.count()} rows")

orders = trim_strings(read_bronze("orders"))
for c in ["order_purchase_timestamp","order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]:
    orders = orders.withColumn(c, F.to_timestamp(c))
save(deduplicate(orders, ["order_id"]), "orders")

customers = trim_strings(read_bronze("customers"))  # Keep ZIP prefixes as strings to preserve leading zeros
save(deduplicate(customers, ["customer_id"]), "customers")

items = trim_strings(read_bronze("order_items"))
items = (items.withColumn("order_item_id", F.col("order_item_id").cast(IntegerType()))
    .withColumn("shipping_limit_date", F.to_timestamp("shipping_limit_date"))
    .withColumn("price", F.col("price").cast(DoubleType()))
    .withColumn("freight_value", F.col("freight_value").cast(DoubleType())))
save(deduplicate(items, ["order_id","order_item_id"]), "order_items")

payments = trim_strings(read_bronze("order_payments"))
payments = (payments.withColumn("payment_sequential", F.col("payment_sequential").cast(IntegerType()))
    .withColumn("payment_installments", F.col("payment_installments").cast(IntegerType()))
    .withColumn("payment_value", F.col("payment_value").cast(DoubleType())))
save(deduplicate(payments, ["order_id","payment_sequential"]), "order_payments")

reviews = trim_strings(read_bronze("order_reviews"))
reviews = (reviews.withColumn("review_score", F.col("review_score").cast(IntegerType()))
    .withColumn("review_creation_date", F.to_timestamp("review_creation_date"))
    .withColumn("review_answer_timestamp", F.to_timestamp("review_answer_timestamp")))
save(deduplicate(reviews, ["review_id"]), "order_reviews")

products = trim_strings(read_bronze("products"))
for c in ["product_name_lenght","product_description_lenght","product_photos_qty","product_weight_g","product_length_cm","product_height_cm","product_width_cm"]:
    products = products.withColumn(c, F.col(c).cast(IntegerType()))
save(deduplicate(products, ["product_id"]), "products")

sellers = trim_strings(read_bronze("sellers"))  # Keep ZIP prefixes as strings to preserve leading zeros
save(deduplicate(sellers, ["seller_id"]), "sellers")

geo = trim_strings(read_bronze("geolocation"))
geo = (geo.withColumn("geolocation_lat", F.col("geolocation_lat").cast(DoubleType()))
    .withColumn("geolocation_lng", F.col("geolocation_lng").cast(DoubleType())))
geo = geo.groupBy("geolocation_zip_code_prefix","geolocation_city","geolocation_state").agg(
    F.avg("geolocation_lat").alias("latitude"), F.avg("geolocation_lng").alias("longitude"))
save(geo, "geolocation_by_zip")

translation = trim_strings(read_bronze("category_translation"))
save(translation, "category_translation")
