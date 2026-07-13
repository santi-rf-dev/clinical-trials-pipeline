# Bonus Questions

## 1. Scalability: How would you modify your solution to handle 100x more data volume?

To support significantly larger data volumes, I would evolve the current architecture by:

- implementing incremental loading instead of full refresh
- processing data in batches instead of loading everything into memory
- replacing pandas with PySpark for distributed processing if required
- partitioning large database tables

These changes would allow the pipeline to scale while reducing execution time and database load.

---

## 2. Data Quality: What additional data validation rules would you implement for clinical trial data?

Additional validation rules could include:

- validating that completion dates are not earlier than start dates
- validating allowed values for study status and study type
- validating geographic coordinates against country information
- validating that mandatory identifiers are present
- generating data quality reports with validation metrics

---

## 3. Compliance: If this were a GxP environment, what additional considerations would you need?

If this pipeline were used in a GxP-regulated environment, the main objective would be to ensure that every execution is traceable, reproducible and auditable.

Additional considerations would include:

- keeping an audit trail of every pipeline execution
- versioning the ETL code
- recording the ingestion timestamp for each pipeline execution
- documenting and approving changes before deployment
- restricting access through role-based permissions
- protecting sensitive data using encryption and secure authentication

These practices help ensure that the generated data can be trusted and reproduced if required by regulatory authorities.

---

## 4. Monitoring: How would you monitor this pipeline in production?

In a production environment, I would monitor both the health of the pipeline and the quality of the processed data.

Key monitoring metrics would include:

- **Pipeline execution status** to detect failed or incomplete executions.
- **Execution time** to identify performance degradations over time.
- **Number of processed records** to detect unexpected drops or spikes in incoming data.
- **API failures and retry attempts** to detect connectivity or availability issues with the data source.
- **Database loading errors** to ensure data is successfully persisted.

These metrics could be integrated with monitoring platforms such as Azure Monitor, with alerts configured for failed executions or abnormal behaviour.

---

## 5. Security: What security measures would you implement for sensitive clinical data?

For sensitive clinical data, I would implement:

- protecting sensitive data using encryption both in transit and at rest
- managing credentials and API secrets using a secure vault such as Azure Key Vault
- applying the principle of least-privilege database access
- centralized authentication and authorization through Microsoft Entra ID, avoiding shared credentials whenever possible
- comprehensive logging and auditing