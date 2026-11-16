
-- ============================================================
-- BANKING DATA PIPELINE
-- PostgreSQL Database Schema
-- ============================================================
-- Project: Understanding the Data Pipeline
-- Purpose: Educational use with synthetic banking data
--
-- This script creates three related database tables.
-- It does not delete existing tables.
-- ============================================================


-- ============================================================
-- 1. CUSTOMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    nric_number VARCHAR(30),
    phone_number VARCHAR(30),
    date_of_birth DATE,
    gender VARCHAR(10),
    created_date DATE NOT NULL
);


-- ============================================================
-- 2. ACCOUNTS
-- ============================================================

CREATE TABLE IF NOT EXISTS accounts (
    account_number VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    account_type VARCHAR(30) NOT NULL,
    current_balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    account_status VARCHAR(15) NOT NULL,
    opened_date DATE NOT NULL,

    CONSTRAINT fk_accounts_customers
        FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON DELETE RESTRICT
);


-- ============================================================
-- 3. TRANSACTIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(30) PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,

    CONSTRAINT fk_transactions_accounts
        FOREIGN KEY (account_number)
        REFERENCES accounts (account_number)
        ON DELETE RESTRICT
);
