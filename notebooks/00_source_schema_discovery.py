# Microsoft Fabric notebook — source schema discovery
# Run after placing the approved e-commerce CSV dataset in Files/landing/ecommerce/.
# This produces an inventory for designing accurate Silver transformations.

from pyspark.sql import functions as F

SOURCE_PATH = "Files/landing/ecommerce/"
df = (spark.read
    .option("header", True)
    .option("inferSchema", False)
    .option("mode", "PERMISSIVE")
    .csv(SOURCE_PATH))

if not df.columns:
    raise ValueError(f"No columns found at {SOURCE_PATH}; check the landing path and CSV headers.")

print("Discovered columns (raw CSV values are strings):")
for field in df.schema.fields:
    print(f"- {field.name}: {field.dataType.simpleString()}")

print(f"Sample row count: {df.count()}")
display(df.limit(20))

# Before implementation, record:
# 1) source dataset URL/license and file list
# 2) table grain and primary/business key for each file
# 3) date/time fields and timezone assumptions
# 4) relationship keys and cardinality
# 5) null/duplicate expectations and business KPI definitions
