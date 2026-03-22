-- =============================================
-- Step 1: Create schema for Sports Betting CDP
-- =============================================
CREATE SCHEMA IF NOT EXISTS SPORT_BETTING_CDP;

-- =============================================
-- Step 2: Create table: user_devices
-- Purpose : Tracks devices used by users
-- =============================================
CREATE TABLE SPORT_BETTING_CDP.user_devices (
    device_id      UUID,          -- Unique identifier for the device
    user_id        VARCHAR,       -- Foreign key reference to the user
    device_type    VARCHAR,       -- Type of device (e.g., iPhone, Android)
    ip_address     VARCHAR,       -- IP address of the device
    last_used      VARCHAR        -- Timestamp (string format) of last usage
);

-- =============================================
-- Step 3: Create table: transactions
-- Purpose : Records deposit and withdrawal activity
-- =============================================
CREATE TABLE SPORT_BETTING_CDP.transactions (
    txn_id          VARCHAR PRIMARY KEY,  -- Unique transaction identifier
    user_id         VARCHAR,              -- Foreign key reference to the user
    txn_type        VARCHAR,              -- Type of transaction (Deposit or Withdrawal)
    amount          DECIMAL(10,2),        -- Monetary value of the transaction
    payment_method  VARCHAR,              -- Method used for payment (e.g., Visa, PayPal)
    status          VARCHAR,              -- Current status of the transaction (e.g., Pending, Completed)
    txn_time        VARCHAR               -- Timestamp (string format) of the transaction
);


