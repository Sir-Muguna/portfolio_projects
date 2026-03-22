
# 📘 CDP Combined Table Documentation: `transactions` & `user_devices`

---

## 📦 1. Source Layer: PostgreSQL ➝ Bronze

**Ingestion Mechanism:** On-Prem PostgreSQL → Microsoft Fabric Lakehouse

| Table           | Bronze Path                                              |
|----------------|-----------------------------------------------------------|
| `transactions`  | `cdp_bronze/postgresql/transactions_<timestamp>.parquet` |
| `user_devices`  | `cdp_bronze/postgresql/user_devices_<timestamp>.parquet` |

---

## 🧱 2. Silver Layer: Cleansing, Standardization

### 📑 Table: `stg_transactions`

**Key Transformations:**

| Step                     | Details |
|--------------------------|---------|
| Normalize `txn_type`     | Map variations like `Wd`, `withdraw` to `'Withdrawal'` |
| Standardize `status`     | Map to: `'Completed'`, `'Pending'`, `'Failed'` |
| Parse `txn_time`         | Convert to `TIMESTAMP`, handle multiple formats |
| Filter invalid rows      | Remove `amount <= 0`, NULL `txn_id`, empty fields |
| Deduplicate              | Use `ROW_NUMBER()` on `txn_id` |
| Add metadata             | `ingestion_time`, `pipeline_run_id`, `source` |

**Data Quality Checks:**

- `txn_id` IS NOT NULL AND UNIQUE
- `amount > 0`
- `status` IN [`Completed`, `Pending`, `Failed`]
- `txn_time` IS TIMESTAMP AND NOT FUTURE-DATED

---

### 📑 Table: `stg_user_devices`

**Key Transformations:**

| Step                      | Details |
|---------------------------|---------|
| Normalize `device_type`   | Lowercase, map to standard list (e.g., "smart toaster" ➝ `"Other"`) |
| Parse `last_used`         | Handle multiple timestamp formats, convert to `TIMESTAMP` |
| Validate `ip_address`     | Filter malformed IPs (`localhost`, `'abc.def.ghi.jkl'`, etc.) |
| Deduplicate               | Based on `device_id` |
| Add metadata              | `ingestion_time`, `pipeline_run_id`, `source` |

**Data Quality Checks:**

- `device_id` IS NOT NULL AND UNIQUE
- `ip_address` must match regex for IPv4
- `last_used` must parse to valid `TIMESTAMP`
- `device_type` IN accepted list or mapped to `"Other"`

---

## 🥇 3. Gold Layer: Business Curated Tables

### 📊 Table: `fct_transactions`

| Logic/Enhancement         | Description |
|---------------------------|-------------|
| Filter by status          | Keep only `Completed` |
| Join with dimensions      | `dim_users`, `payment_method_dim` |
| Derived fields            | Revenue metrics, volume |
| Ensure FK consistency     | On `user_id` |

**Gold-Level DQ Checks:**

- `txn_id` uniqueness
- `user_id` exists in `dim_users`
- No NULLs in key columns
- No future `txn_time`

---

### 📊 Table: `dim_user_devices`

| Logic/Enhancement         | Description |
|---------------------------|-------------|
| Enrich device info        | Normalize and tag unusual devices |
| Retain latest usage       | Optional: `ROW_NUMBER() OVER (...)` to keep most recent per user |
| Validate recency          | Optional: Filter out inactive > 1 year |
| Link to user dimension    | Via `user_id` FK |

**Gold-Level DQ Checks:**

- Device usage must be within last 2 years
- All `user_id`s must exist in `dim_users`
- IPs are real-world routable (not private/loopback/local)

---

## 📁 Directory Structure

```bash
cdp_bronze/
  └─ postgresql/
      ├─ transactions_*.parquet
      └─ user_devices_*.parquet

cdp_silver/
  ├─ stg_transactions/
  └─ stg_user_devices/

cdp_gold/
  ├─ fct_transactions/
  └─ dim_user_devices/
```

---

## 🛠 Tooling Stack

| Process              | Tool                     |
|----------------------|--------------------------|
| Ingestion            | Fabric Gateway Connector |
| Silver Transform     | PySpark / dbt            |
| Gold Layer Logic     | dbt                      |
| Quality Validation   | dbt tests, PySpark       |
| Storage              | Fabric Lakehouse         |

---

## 🧪 Summary of Quality Rules by Table

| Table             | Validation Rules |
|------------------|------------------|
| `stg_transactions` | Non-null ID, positive `amount`, status normalization, timestamp parsing |
| `stg_user_devices` | Valid `ip_address`, parse `last_used`, normalize `device_type` |
| `fct_transactions` | FK constraints, completed status, derived fields |
| `dim_user_devices` | Device uniqueness, recent activity, valid IP and FK |
