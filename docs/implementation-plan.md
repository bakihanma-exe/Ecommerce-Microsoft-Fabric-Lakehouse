# Fabric E-Commerce Lakehouse — implementation plan

## Current confirmed scope
The resume material supports ADF ingestion to ADLS Gen2, Microsoft Fabric Lakehouse, Fabric notebooks using PySpark/Spark SQL, and Bronze/Silver/Gold processing with cleansing, deduplication, aggregation and quality checks.

## Dataset discovery gate
No exact dataset, source URL, license, file list, column schema, table grain, business key, modified timestamp or KPI definition is confirmed. Do not silently substitute a public dataset or invent column names.

1. Obtain approval for the source dataset and confirm redistribution/use terms.
2. Record each source file, exact header, sample values, row count and file format.
3. Identify each table's grain, business key, foreign keys and relationship cardinality.
4. Identify reliable change tracking (modified timestamp, sequence or CDC) before designing incremental loads.
5. Agree KPI formulas and reporting grain with the business.

## Notebook execution order
1. Place approved source files in the Fabric Lakehouse Files landing folder.
2. Run `notebooks/00_source_schema_discovery.py` and record the discovered headers and sample values.
3. Run `notebooks/01_bronze_ingestion.py` for a full-refresh Bronze Delta snapshot.
4. Implement explicit Silver casts, standardization, deduplication and reject handling only after keys and types are confirmed.
5. Implement Gold aggregates only after KPI formulas and grain are agreed.
6. Run `sql/data_quality_checks.sql` after replacing its commented example checks with confirmed source keys and constraints.

## Reliability / production checklist
- Use explicit schemas and schema-drift handling after discovery.
- Make retries idempotent; use a stable batch ID or source watermark if incremental ingestion is supported.
- Advance watermarks only after all relevant copy and validation steps succeed.
- Quarantine invalid records with reason codes; do not silently discard them.
- Log pipeline/notebook run IDs, source file, status, counts and duration.
- Configure Fabric workspace connections and permissions without embedding secrets.
- Add orchestration, monitoring, alerting and CI/CD only after workspace and deployment requirements are known.

## Honest status
The repository is a schema-neutral starter. It is not an end-to-end implementation until the dataset is selected, transformations are bound to its schema, and the notebooks are executed in a configured Fabric workspace.
