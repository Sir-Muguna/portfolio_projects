
# **Combined Transformation and Documentation Process for `transactions` and `user_devices` Tables**

---

## 🔹 Overview

This document outlines the structured data processing workflow for the `transactions` and `user_devices` tables stored in PostgreSQL. The transformation process adheres to a **Bronze → Silver → Gold** data architecture and incorporates:

- **Idempotency**
- **Data Lineage Tracking**
- **Referential Integrity**
- **Schema Evolution Handling**
- **Data Quality Rules**

---

## 🔸 Source Tables

### `transactions` Table (PostgreSQL)
- Captures user transactions such as purchases or activity logs.
- Key columns: `transaction_id`, `user_id`, `transaction_type`, `timestamp`, `amount`, `status`.

### `user_devices` Table (PostgreSQL)
- Contains metadata on user-linked devices.
- Key columns: `device_id`, `user_id`, `device_type`, `ip_address`, `last_used`.

---

## 🔸 Transformation Layers

### 1. **Bronze Layer** – Raw Ingestion

- **Goal**: Ingest raw data from PostgreSQL into Delta Lake.
- **Actions**:
  - Load without transformations for full fidelity.
  - Append mode used to retain history.
- **Data Quality Checks**:
  - None at this stage to preserve raw input.
- **Schema Evolution Handling**:
  - Schema inferred; changes tracked using Delta Lake’s `mergeSchema`.

---

### 2. **Silver Layer** – Cleansed & Conformed

#### 🔹 Actions Applied:
- Standardize column names (`snake_case`, lowercase).
- Convert timestamps to consistent format (`yyyy-MM-dd HH:mm:ss`).
- Remove/flag malformed IPs (`user_devices`).
- Cast data types (e.g., `amount` as decimal, `timestamp` as timestamp).
- Normalize categorical fields (e.g., `device_type`, `transaction_type`).
- Deduplicate records using `ROW_NUMBER` with partitioning keys.

#### 🔹 Idempotency Measures:
- Use `MERGE INTO` based on primary keys (e.g., `transaction_id`, `device_id`).
- Deterministic transformations ensure repeatable outcomes.

#### 🔹 Data Quality Rules Implemented:
| Rule | Table | Column(s) | Rule Description |
|------|-------|-----------|------------------|
| Null Checks | both | `user_id` | Reject rows with null `user_id`. |
| Format Check | `user_devices` | `ip_address` | Filter malformed IPs using regex validation. |
| Range Check | `transactions` | `amount` | Ensure amount > 0 and < business-defined upper bound. |
| Categorical Validation | both | `transaction_type`, `device_type` | Allow only valid enum values. |
| Timestamp Validity | both | `timestamp`, `last_used` | Exclude future timestamps. |

#### 🔹 Referential Integrity:
- Enforced between `transactions.user_id` and `user_devices.user_id`.
- Records failing FK checks can be logged in a quarantine table for review.

#### 🔹 Schema Evolution:
- Auto-schema merge enabled with strict column renaming strategy.
- New columns added in a controlled manner with change logging.

---

### 3. **Gold Layer** – Business-Ready Models

#### 🔹 Purpose:
- Create analytical, reporting-ready datasets with metrics and KPIs.

#### 🔹 Transformations:
- Aggregate metrics: total transactions per user/device.
- Join datasets on `user_id` to enrich data.
- Derive device activity trends (`last_used` by device_type).
- Add surrogate keys and dimensional IDs if needed (e.g., `date_id`).

#### 🔹 Data Quality (Continued Validation):
- Recheck for nulls and unexpected joins.
- Verify aggregation accuracy.
- Validate row-level constraints after joins.

#### 🔹 Data Lineage:
- Tracked via dbt’s `source`, `ref`, and model relationships.
- Stored as DAGs for visual traceability.

---

## 🔸 Best Practices Summary

| Practice | Description |
|---------|-------------|
| **Modular Pipelines** | Separate logic for each layer (Bronze/Silver/Gold). |
| **Idempotent Jobs** | Use `MERGE`, not append-only logic, to prevent duplication. |
| **Centralized Quality Rules** | Apply reusable constraints across transformations. |
| **Schema Control** | Versioning and governance for changes. |
| **Observability** | Include logging, metrics, and lineage tracking in each layer. |
| **Quarantine Invalid Data** | Store rejected data separately for review. |
