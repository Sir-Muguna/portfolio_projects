## Project Overview

| Property | Value |
| :--- | :--- |
| **Client** | [Client Name] |
| **Project** | Dynamic 3-5 Year Financial Forecast & Dashboard |
| **Goal** | Build a scalable, data-driven financial operating system to support investor discussions and strategic planning. |
| **Core Stack** | Airbyte, dbt, BigQuery, Airflow, Superset, Docker |
| **Project Lead** | [Your Name/Company] |
| **Start Date** | [Date] |
| **Status** | `Not Started` |

---

## Master Task Database (Table View)

This is your main project tracker. Each task is linked to its Phase and Sprint.

| Task | Phase | Sprint | Status | Assignee | Due Date | Client Engagement |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Kickoff & Data Discovery** | 0. Foundation & Discovery | Week 1 | `Done` | Lead | [Date] | **High** |
| **Finalize Scope & Success Metrics** | 0. Foundation & Discovery | Week 1 | `Done` | Lead | [Date] | **High** |
| **Compile Data Source List** | 0. Foundation & Discovery | Week 1 | `Done` | Lead | [Date] | **High** |
| **Draft Architecture Diagram** | 0. Foundation & Discovery | Week 2 | `Done` | Lead | [Date] | **Medium** |
| **Finalize config.yml structure** | 0. Foundation & Discovery | Week 2 | `Done` | Lead | [Date] | **Medium** |
| **Provision Cloud Resources (GCP, BigQuery)** | 0. Foundation & Discovery | Week 2 | `Done` | Lead | [Date] | **None** |
| **Dockerize Local Dev Environment** | 0. Foundation & Discovery | Week 2 | `Done` | Lead | [Date] | **None** |
| **Build Airbyte Connectors** | 1. Data Pipeline | Week 3 | `In Progress` | Lead | [Date] | **Low** |
| **Validate Raw Data in Staging** | 1. Data Pipeline | Week 3 | `To Do` | Lead | [Date] | **Low** |
| **Write Initial Data Quality Checks** | 1. Data Pipeline | Week 3 | `To Do` | Lead | [Date] | **None** |
| **...** | ... | ... | ... | ... | ... | ... |
| **Build dbt model: int_occupancy_forecast** | 1. Data Pipeline | Week 4 | `To Do` | Lead | [Date] | **None** |
| **Build dbt model: int_revenue_calculations** | 1. Data Pipeline | Week 4 | `To Do` | Lead | [Date] | **None** |
| **...** | ... | ... | ... | ... | ... | ... |
| **Client UAT & Sign-off** | 2. Visualization & Validation | Week 9 | `To Do` | Lead | [Date] | **Very High** |
| **Draft Maintenance Plan & Retainer** | 3. Launch & Future-Proofing | Week 12 | `To Do` | Lead | [Date] | **High** |
---

## Phase Database (Grouped by Phase)

### **Phase 0: Foundation & Discovery (Weeks 1-2)**
*Objective: Align on vision, gather all requirements, and set up the core infrastructure.*

| Task | Sprint | Status | Client Engagement |
| :--- | :--- | :--- | :--- |
| **Kickoff & Data Discovery** | Week 1 | `Done` | **High** |
| **Finalize Scope & Success Metrics** | Week 1 | `Done` | **High** |
| **Compile Data Source List** | Week 1 | `Done` | **High** |
| **Draft Architecture Diagram** | Week 2 | `Done` | **Medium** |
| **Finalize config.yml structure** | Week 2 | `Done` | **Medium** |
| **Provision Cloud Resources (GCP, BigQuery)** | Week 2 | `Done` | **None** |
| **Dockerize Local Dev Environment** | Week 2 | `Done` | **None** |
| **Set up CI/CD pipeline skeleton** | Week 2 | `Done` | **None** |

### **Phase 1: Data Pipeline Construction (Weeks 3-6)**
*Objective: Build the robust ETL pipelines that form the engine of the forecast.*

| Task | Sprint | Status | Client Engagement |
| :--- | :--- | :--- | :--- |
| **Build and test Airbyte connections** | Week 3 | `In Progress` | **Low** |
| **Validate raw data landing in staging** | Week 3 | `To Do` | **Low** |
| **Write initial data quality checks** | Week 3 | `To Do` | **None** |
| **Build dbt staging models (stg_*)** | Week 4 | `To Do` | **None** |
| **Build dbt model: int_occupancy_forecast** | Week 4 | `To Do` | **None** |
| **Build dbt model: int_revenue_calculations** | Week 4 | `To Do` | **None** |
| **Build dbt models for costs (int_staffing_costs, etc.)** | Week 5 | `To Do` | **None** |
| **Build final fact models (fct_income_statement)** | Week 5 | `To Do` | **None** |
| **Calculate final KPIs (EBITDA, Break-Even)** | Week 5 | `To Do` | **None** |
| **Build master Airflow DAG** | Week 6 | `To Do` | **None** |
| **Implement error handling & alerts** | Week 6 | `To Do` | **None** |
| **Conduct end-to-end pipeline test** | Week 6 | `To Do` | **Medium** |

### **Phase 2: Visualization & Client Validation (Weeks 7-9)**
*Objective: Build the client-facing interface and validate the model's accuracy.*

| Task | Sprint | Status | Client Engagement |
| :--- | :--- | :--- | :--- |
| **Connect Superset to BigQuery** | Week 7 | `To Do` | **None** |
| **Build main executive dashboard** | Week 7 | `To Do` | **High** |
| **Implement Row-Level Security (RLS)** | Week 7 | `To Do` | **None** |
| **Build "scenario selector" in dashboard** | Week 8 | `To Do` | **Very High** |
| **Pressure-test model with client** | Week 8 | `To Do` | **Very High** |
| **Iterate on models based on feedback** | Week 8 | `To Do` | **Very High** |
| **Grant client user access** | Week 9 | `To Do` | **High** |
| **Provide user training & create guide** | Week 9 | `To Do` | **High** |
| **Client UAT & Sign-off** | Week 9 | `To Do` | **Very High** |

### **Phase 3: Launch & Future-Proofing (Weeks 10-12)**
*Objective: Hand over the system and establish a framework for long-term retention.*

| Task | Sprint | Status | Client Engagement |
| :--- | :--- | :--- | :--- |
| **Deploy all code to production** | Week 10 | `To Do` | **None** |
| **Run full production data pipeline** | Week 10 | `To Do` | **Medium** |
| **Final security review** | Week 10 | `To Do` | **None** |
| **Draft Maintenance & Operations Guide** | Week 10 | `To Do` | **None** |
| **Finalize technical documentation** | Week 11 | `To Do` | **Low** |
| **Record system walkthrough videos** | Week 11 | `To Do` | **None** |
| **Draft Maintenance Plan & Retainer** | Week 12 | `To Do` | **High** |
| **Present retainer proposal** | Week 12 | `To Do` | **High** |
| **Schedule first Quarterly Business Review** | Week 12 | `To Do` | **High** |

---

## Sprint Database (Grouped by Week)

### **Sprint: Week 1**
**Focus:** Kickoff & Data Discovery

| Task | Phase | Status |
| :--- | :--- | :--- |
| **Kickoff & Data Discovery** | 0. Foundation & Discovery | `Done` |
| **Finalize Scope & Success Metrics** | 0. Foundation & Discovery | `Done` |
| **Compile Data Source List** | 0. Foundation & Discovery | `Done` |

### **Sprint: Week 2**
**Focus:** Technical Design & Setup

| Task | Phase | Status |
| :--- | :--- | :--- |
| **Draft Architecture Diagram** | 0. Foundation & Discovery | `Done` |
| **Finalize config.yml structure** | 0. Foundation & Discovery | `Done` |
| **Provision Cloud Resources (GCP, BigQuery)** | 0. Foundation & Discovery | `Done` |
| **Dockerize Local Dev Environment** | 0. Foundation & Discovery | `Done` |
| **Set up CI/CD pipeline skeleton** | 0. Foundation & Discovery | `Done` |

### **Sprint: Week 3**
**Focus:** Data Ingestion (Airbyte)

| Task | Phase | Status |
| :--- | :--- | :--- |
| **Build and test Airbyte connections** | 1. Data Pipeline | `In Progress` |
| **Validate raw data landing in staging** | 1. Data Pipeline | `To Do` |
| **Write initial data quality checks** | 1. Data Pipeline | `To Do` |

*(...and so on for each subsequent week...)*

---

## Client Deliverables Database (Kanban Board View)

| Deliverable | Phase | Due Date | Status |
| :--- | :--- | :--- | :--- |
| **Signed Project Charter** | 0. Foundation & Discovery | [Date] | `Done` ✅ |
| **Approved Architecture Diagram** | 0. Foundation & Discovery | [Date] | `Done` ✅ |
| **Demo of Automated Pipeline** | 1. Data Pipeline | [Date] | `Ready` ◻️ |
| **Initial Dashboard Prototype** | 2. Visualization & Validation | [Date] | `Ready` ◻️ |
| **Validated "Base Case" Forecast** | 2. Visualization & Validation | [Date] | `Ready` ◻️ |
| **Signed UAT Approval** | 2. Visualization & Validation | [Date] | `Ready` ◻️ |
| **Complete Project Documentation** | 3. Launch & Future-Proofing | [Date] | `Ready` ◻️ |
| **Signed Retainer Agreement** | 3. Launch & Future-Proofing | [Date] | `Ready` ◻️ |