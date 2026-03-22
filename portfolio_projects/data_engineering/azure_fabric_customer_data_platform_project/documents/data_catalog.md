# Data Catalog for Gold Layer

## Overview
The Gold Layer is the business-level data representation, structured to support analytical and reporting use cases.  
It consists of **dimension tables** and **fact tables** designed to serve specific business metrics.

---

## 1. gold.dim_customers

**Purpose:**  
Stores customer profile details enriched with demographic, behavioral, and preference data.

**Columns:**

| Column Name           | Data Type       | Description |
|------------------------|----------------|-------------|
| customer_key           | INT            | Surrogate key uniquely identifying each customer. |
| user_id                | STRING         | Original user identifier from the source systems. |
| username               | STRING         | User’s system login name. |
| email                  | STRING         | User email address. |
| first_name             | STRING         | First name of the user. |
| last_name              | STRING         | Last name of the user. |
| date_of_birth          | DATE           | Date of birth. |
| registration_date      | DATE           | When the user registered. |
| country_code           | STRING         | User’s country (e.g., 'KE', 'NG', 'ZA'). |
| kyc_status             | STRING         | KYC verification status. |
| account_status         | STRING         | User’s account lifecycle state. |
| favorite_sport         | STRING         | Most preferred sport for betting. |
| odds_format            | STRING         | Odds format selected by the user. |
| marketing_opted_in     | BOOLEAN        | Marketing consent status. |
| device_count           | INT            | Total number of devices used. |
| last_device_type       | STRING         | Last device type used (e.g., 'Mobile', 'Desktop'). |
| last_ip_address        | STRING         | Last seen IP address. |
| profile_load_timestamp | DATETIME       | When the profile was last updated in the gold layer. |

---

## 2. gold.fact_user_transactions

**Purpose:**  
Tracks user monetary behavior: deposits, withdrawals, transaction volumes, and preferences.

**Columns:**

| Column Name           | Data Type   | Description |
|------------------------|------------|-------------|
| transaction_key        | INT        | Surrogate key for transaction record. |
| user_id                | STRING     | Associated user identifier. |
| total_deposits         | FLOAT      | Cumulative deposits by user. |
| total_withdrawals      | FLOAT      | Cumulative withdrawals by user. |
| number_of_transactions | INT        | Total number of transactions made. |
| average_transaction    | FLOAT      | Average amount per transaction. |
| last_transaction_time  | DATETIME   | Most recent transaction timestamp. |
| preferred_payment_method | STRING   | Most commonly used payment method. |
| transaction_load_timestamp | DATETIME | Time of load into the gold layer. |

---

## 3. gold.fact_betting_summary

**Purpose:**  
Captures user betting activity, habits, and risk profile indicators.

**Columns:**

| Column Name           | Data Type   | Description |
|------------------------|------------|-------------|
| betting_summary_key    | INT        | Surrogate key for betting record. |
| user_id                | STRING     | Linked user. |
| total_bets             | INT        | Total number of bets placed. |
| total_staked           | FLOAT      | Total money staked. |
| average_stake          | FLOAT      | Average stake amount. |
| average_odds           | FLOAT      | Average odds of bets placed. |
| win_rate               | FLOAT      | Proportion of bets won. |
| bet_conversion_rate    | FLOAT      | Bets placed per registration. |
| favorite_league        | STRING     | League most bet on. |
| preferred_channel      | STRING     | Channel most frequently used (Web/Mobile). |
| betting_load_timestamp | DATETIME   | Time of load into gold layer. |

---

## 4. gold.fact_match_analytics

**Purpose:**  
Aggregates betting and odds behavior for each match.

**Columns:**

| Column Name           | Data Type   | Description |
|------------------------|------------|-------------|
| match_key              | INT        | Surrogate key for match record. |
| match_id               | STRING     | Unique match identifier. |
| sport                  | STRING     | Type of sport. |
| league                 | STRING     | League name. |
| match_start_time       | DATETIME   | Start time of the match. |
| total_bets             | INT        | Number of bets placed on the match. |
| total_payout           | FLOAT      | Total amount paid out to users. |
| average_odds           | FLOAT      | Avg odds across all markets. |
| odds_volatility_score  | FLOAT      | Calculated odds fluctuation score. |
| final_outcome          | STRING     | Match result (Win/Loss/Draw). |
| match_load_timestamp   | DATETIME   | Load time to gold layer. |

---

## 5. gold.fact_odds_movement

**Purpose:**  
Monitors how odds evolve over time during a match for volatility analysis.

**Columns:**

| Column Name           | Data Type   | Description |
|------------------------|------------|-------------|
| odds_movement_key      | INT        | Surrogate key. |
| match_id               | STRING     | Related match. |
| market                 | STRING     | Betting market (1X2, Over/Under). |
| start_odds_home        | FLOAT      | Initial odds for home team. |
| end_odds_home          | FLOAT      | Latest odds for home team. |
| odds_volatility_score  | FLOAT      | Computed fluctuation metric. |
| last_update_time       | DATETIME   | Latest odds update timestamp. |

---

## 6. gold.dim_user_segments

**Purpose:**  
Defines user segments based on activity, value, and behavior for personalization and marketing.

**Columns:**

| Column Name           | Data Type   | Description |
|------------------------|------------|-------------|
| segment_key            | INT        | Surrogate key. |
| user_id                | STRING     | Targeted user. |
| segment_name           | STRING     | Segment label (e.g., 'High Value', 'Inactive'). |
| risk_profile           | STRING     | Risk appetite indicator (e.g., 'High Risk'). |
| betting_style          | STRING     | Aggressive, casual, etc. |
| engagement_score       | FLOAT      | Derived engagement metric. |
| last_active_date       | DATE       | Last time the user placed a bet. |
| segment_load_timestamp | DATETIME   | Load time to gold layer. |

---
