# 📘 Project Documentation: Azure Fabric Customer Data Platform for Sports Betting

## 1. Overview
This document details the architecture, processes, components, and design decisions behind the Azure Fabric Customer Data Platform (CDP) developed for a sports betting company. The CDP supports both real-time and batch ingestion, enabling unified analytics, customer profiling, and operational intelligence.

---

## 2. Business Goals
- Unify fragmented customer data into a single source of truth
- Enable real-time fraud detection using live betting feeds
- Support hyper-personalized marketing via enriched behavioral data
- Provide a robust historical archive for analytics and ML modeling

---

## 3. Architecture Summary

### Lakehouse Layers
- **Bronze Layer**: Raw ingested data (streaming + batch)
- **Silver Layer**: Cleaned, deduplicated, and standardized data
- **Gold Layer**: Modeled fact and dimension tables for analytics

### Streaming Stack
- **Kafka Producers**: Python scripts simulate real-time sports betting events
- **Fabric Eventstream**: Ingests Kafka messages and routes to KQL DB + Lakehouse
- **KQL DB**: Hot telemetry zone with TTL (~2 days)

### Batch Stack
- **Source**: Oracle and PostgreSQL databases
- **Fabric Data Pipeline (Dataflows Gen2)**: Copies raw tables into OneLake
- **Dynamic SQL**: Handles source-type branching (Oracle/PostgreSQL)

---

## 4. Ingestion Logic

### Oracle / PostgreSQL Ingestion:
- Uses `@equals(item().sourceType, 'Oracle')` logic
- Constructs queries with:
```js
@concat('SELECT * FROM "', toUpper(item().schema), '"."', toUpper(item().table), '"')
```
- File Naming Convention:
```bash
cdp_bronze/oracle/raw/users_20250711083000.parquet
cdp_bronze/postgresql/raw/transactions_20250711083000.parquet
```

### Kafka Streaming:
- Events: `betting_events`, `match_metadata`, `live_odds_updates`, `bet_results`
- Routed to:
  - **KQL DB**: For live monitoring dashboards
  - **Bronze Layer**: For historical aggregation and downstream ML

---

## 5. Data Transformation Steps

### In Silver Layer (via PySpark Notebooks):
- Normalize date formats (`date_of_birth`, `registration_date`)
- Clean email and username fields (regex, trimming)
- Enforce valid `kyc_status` and `account_status` mappings
- Deduplicate using `user_id` + `load_timestamp`
- Join & enrich with lookup tables

### Data Validation:
- Drop invalid combinations (e.g. `kyc_status = Unknown`)
- Ensure `registration_date` > `date_of_birth`
- Flag nulls in key attributes (username, country)

---

## 6. Gold Layer Dimensional Models

### `gold.dim_customers`
- User-level info: demographics, country, preferences
- Derived fields: age, opt-in status, kyc status

### `gold.fact_user_transactions`
- Daily aggregates of deposits, withdrawals, and balances

### `gold.fact_betting_summary`
- Bet volume, frequency, average risk factor

### `gold.fact_match_analytics`
- Match-specific stats: bet counts, high-risk users, winning odds

### `gold.fact_odds_movement`
- Tracks odds changes over match lifetime for volatility prediction

### `gold.dim_user_segments`
- Rule-based segmentation: High Value, Casual, Risky, Inactive

---

## 7. Monitoring & Observability
- **KQL Dashboards**: Real-time match telemetry and user activity
- **Power BI**: High-level summaries, filters by match/user ID
- **Notebook Logs**: Cell-level execution traces for debugging

---

## 8. Security & Governance
- Private endpoints to source systems
- Role-based access in Fabric workspaces
- Parquet file ACLs in OneLake

---

## 9. Future Enhancements
- Integrate Great Expectations for automated quality checks
- Use CDC connectors for Oracle/Postgres
- Implement schema registry (Avro/Protobuf)
- Integrate Microsoft Purview for lineage & governance

---

## 10. Maintainer
**Ronald Muguna**  
Data Engineer 
GitHub: [Sir-Muguna](https://github.com/Sir-Muguna)

