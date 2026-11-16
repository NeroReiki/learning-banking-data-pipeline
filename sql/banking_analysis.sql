
-- ============================================================
-- BANKING DATA PIPELINE
-- SQL DATA ANALYSIS
-- ============================================================
-- Purpose: Explore cleaned synthetic banking data
-- Database: PostgreSQL
--
-- Run these queries after the ETL pipeline has loaded
-- the customers, accounts, and transactions tables.
-- ============================================================


-- ============================================================
-- 1. BANKING DATA OVERVIEW
-- ============================================================

-- Count customers, accounts, transactions, and
-- total recorded transaction amount.

SELECT
    (SELECT COUNT(*) FROM customers) AS total_customers,
    (SELECT COUNT(*) FROM accounts) AS total_accounts,
    (SELECT COUNT(*) FROM transactions) AS total_transactions,
    (SELECT COALESCE(SUM(amount), 0) FROM transactions)
        AS total_transaction_volume;


-- ============================================================
-- 2. TOP 10 CUSTOMERS BY TRANSACTION VOLUME
-- ============================================================

SELECT
    c.customer_id,
    c.full_name,
    COUNT(DISTINCT a.account_number) AS total_accounts,
    COUNT(t.transaction_id) AS total_transactions,
    COALESCE(SUM(t.amount), 0) AS total_volume
FROM customers c
JOIN accounts a
    ON c.customer_id = a.customer_id
JOIN transactions t
    ON a.account_number = t.account_number
GROUP BY
    c.customer_id,
    c.full_name
ORDER BY total_volume DESC
LIMIT 10;


-- ============================================================
-- 3. TRANSACTION TYPE BREAKDOWN
-- ============================================================

SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    ROUND(AVG(amount), 2) AS average_amount
FROM transactions
GROUP BY transaction_type
ORDER BY transaction_count DESC;


-- ============================================================
-- 4. ACCOUNTS WITHOUT TRANSACTIONS
-- ============================================================

SELECT
    a.account_number,
    a.customer_id,
    a.account_type,
    a.account_status,
    a.current_balance,
    a.opened_date
FROM accounts a
LEFT JOIN transactions t
    ON a.account_number = t.account_number
WHERE t.transaction_id IS NULL
ORDER BY a.account_number;


-- ============================================================
-- 5. ACCOUNTS WITH RECORDED TRANSACTIONS
-- ============================================================

SELECT
    (SELECT COUNT(*) FROM accounts)
        AS total_accounts,

    (SELECT COUNT(DISTINCT account_number)
     FROM transactions)
        AS accounts_with_transactions;


-- ============================================================
-- 6. MONTHLY TRANSACTION TRENDS
-- ============================================================

SELECT
    DATE_TRUNC('month', transaction_date)::DATE
        AS transaction_month,
    COUNT(*) AS total_transactions,
    SUM(amount) AS monthly_volume
FROM transactions
GROUP BY DATE_TRUNC('month', transaction_date)
ORDER BY transaction_month;


-- ============================================================
-- 7. ACCOUNT STATUS DISTRIBUTION
-- ============================================================

SELECT
    account_status,
    COUNT(*) AS total_accounts,
    SUM(current_balance) AS total_balance
FROM accounts
GROUP BY account_status
ORDER BY total_accounts DESC;
