# Microsoft Fabric notebook template — Bronze full-refresh ingestion
# Place approved source CSVs under the Lakehouse Files landing folder first.
# This starter intentionally does not assume an e-commerce schema or business key.
from pyspark.sql import functions as F

SOURCE_PATH = "Files/landing/ecommerce/"
BRONZE_TABLE = "bronze_ecommerce"

raw_df = (spark.read
    .option("header", True)
    .option("inferSchema", False)
    .option("mode", "FAILFAST")
    .csv(SOURCE_PATH))

if not raw_df.columns:
    raise ValueError(f"No source columns discovered at {SOURCE_PATH}")

bronze_df = (raw_df
    .withColumn("_ingested_at_utc", F.current_timestamp())
    .withColumn("_source_file", F.input_file_name()))

# Full-refresh snapshot: rerunning this notebook replaces the Bronze table
# rather than appending duplicate copies of the same static source files.
(bronze_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(BRONZE_TABLE))

print(f"Bronze rows written: {bronze_df.count()}")
print(f"Bronze columns: {raw_df.columns}")

# After the actual source is confirmed, define explicit types and a stable
# ingestion batch / incremental strategy if the source supports it.
