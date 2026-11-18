# ADF orchestration design for Olist

## Source acquisition
The public source is distributed through Kaggle and requires Kaggle authentication. Do not embed Kaggle tokens in ADF linked services or source control. Download the archive using the local script, then upload the nine CSVs to a secured ADLS Gen2 landing container.

## ADF pipeline
1. Parameterize the ADLS landing container and folder.
2. Use Get Metadata to list the nine expected CSV files or use a configuration table based on `data/source-manifest.json`.
3. ForEach iterates the file list.
4. Copy Activity copies each CSV into the Fabric/ADLS landing path while preserving its filename.
5. Log pipeline run ID, source filename, status, bytes copied, start/end time and error details.
6. On successful copy, trigger the Fabric notebook sequence: Bronze, Silver, Gold.
7. Promote/report only after SQL quality checks pass.

## Load strategy
Olist is a static historical snapshot. Use replace/overwrite for repeatable full refresh. The included notebooks overwrite Bronze Delta tables. Do not claim incremental CDC or a watermark strategy for this dataset.

## Security
Use managed identity for ADLS access where supported. Keep Kaggle credentials outside ADF and outside Git. Grant least-privilege access to the landing and curated locations.
