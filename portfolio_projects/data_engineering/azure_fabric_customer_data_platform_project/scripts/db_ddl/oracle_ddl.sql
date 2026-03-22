-- ===============================================================
-- 🔧 STEP 1: Create dedicated schema/user for the project
-- ===============================================================
ALTER SESSION SET "_ORACLE_SCRIPT"=TRUE;
CREATE USER sport_betting_cdp IDENTIFIED BY "NB/(createownpassword)";

-- Grant roles for DML and DDL operations
GRANT CONNECT, RESOURCE, DBA TO sport_betting_cdp;

-- ===============================================================
-- 📦 STEP 2: Create tables in correct order within the schema
-- ===============================================================

-- Set storage quota for the user (on the USERS tablespace)
ALTER USER sport_betting_cdp QUOTA 200M ON USERS;

-- 📝 Note: Removed quotas on non-existing tablespaces 'KYC_DOCUMENTS' and 'USER_PREFERENCES'

-- ===============================================================
-- 1️⃣ USERS table: Core user identity and profile
-- ===============================================================

CREATE TABLE sport_betting_cdp.users (
    user_id            VARCHAR2(20) PRIMARY KEY,          -- Unique user identifier
    username           VARCHAR2(50),                      -- User's username
    email              VARCHAR2(100),                     -- User's email address
    first_name         VARCHAR2(50),                      -- User's first name
    last_name          VARCHAR2(50),                      -- User's last name
    date_of_birth      VARCHAR2(50),                      -- User's date of birth
    registration_date  VARCHAR2(50),                      -- Registration date
    country_code       VARCHAR2(10),                      -- Country code (ISO 3166-1)
    kyc_status         VARCHAR2(20),                      -- KYC status (e.g., 'Verified', 'Pending')
    account_status     VARCHAR2(20)                       -- Account status (e.g., 'Active', 'Suspended')
);

-- Grant REFERENCES privilege on 'users' table
GRANT REFERENCES ON sport_betting_cdp.users TO sport_betting_cdp;

-- ===============================================================
-- 2️⃣ USER_PREFERENCES: Personalization settings (FK to users)
-- ===============================================================

CREATE TABLE sport_betting_cdp.user_preferences (
    user_id            VARCHAR2(20),                      -- User ID (foreign key to USERS table)
    favorite_sports    CLOB,                               -- User's favorite sports (long text)
    odds_format        VARCHAR2(10),                      -- Preferred odds format (e.g., 'Decimal', 'Fractional')
    marketing_opt_in   VARCHAR2(10),                      -- Marketing opt-in ('Y' or 'N')
    
    -- Foreign key constraint to reference USERS table
    CONSTRAINT fk_user_pref_user 
        FOREIGN KEY (user_id) REFERENCES sport_betting_cdp.users(user_id)
);

-- ===============================================================
-- 3️⃣ KYC_DOCUMENTS: KYC uploads and statuses (FK to users)
-- ===============================================================

CREATE TABLE sport_betting_cdp.kyc_documents (
    document_id        VARCHAR2(200) PRIMARY KEY,         -- Unique document identifier
    user_id            VARCHAR2(20),                      -- User ID (foreign key to USERS table)
    document_type      VARCHAR2(50),                      -- Type of document (e.g., 'Passport', 'Driver's License')
    upload_date        VARCHAR2(50),                      -- Date of document upload
    status             VARCHAR2(20),                      -- KYC status for the document (e.g., 'Pending', 'Verified')
    verified_by        VARCHAR2(100),                     -- Who verified the document
     
    -- Foreign key constraint to reference USERS table
    CONSTRAINT fk_kyc_user 
        FOREIGN KEY (user_id) REFERENCES sport_betting_cdp.users(user_id)
);
