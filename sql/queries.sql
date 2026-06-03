-- ==========================================
-- bluestock_mf.db - Analytical Queries
-- ==========================================

-- 1. Top 5 funds by AUM (Assets Under Management)
SELECT 
    scheme_name, 
    fund_house, 
    aum_crore 
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month for a specific fund (e.g., HDFC Top 100 - 125497)
SELECT 
    strftime('%Y-%m', date) AS month,
    AVG(nav) AS avg_nav
FROM fact_nav
WHERE amfi_code = 125497
GROUP BY month
ORDER BY month;

-- 3. SIP Inflows by Year (To calculate YoY Growth)
SELECT 
    strftime('%Y', transaction_date) AS txn_year,
    COUNT(transaction_id) AS total_sip_count,
    SUM(amount_inr) AS total_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY txn_year
ORDER BY txn_year;

-- 4. Total transaction volume by State
SELECT 
    state,
    COUNT(transaction_id) as total_transactions,
    SUM(amount_inr) as total_volume_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_volume_inr DESC;

-- 5. Funds with an expense ratio strictly less than 1%
SELECT 
    scheme_name, 
    category, 
    expense_ratio_pct 
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- 6. Average 1-Year Return by Risk Category (Joining Dim and Fact)
SELECT 
    d.risk_category,
    ROUND(AVG(p.return_1yr_pct), 2) AS avg_1yr_return
FROM dim_fund d
JOIN fact_performance p ON d.amfi_code = p.amfi_code
GROUP BY d.risk_category
ORDER BY avg_1yr_return DESC;

-- 7. Lumpsum vs. SIP preference by Age Group
SELECT 
    age_group,
    transaction_type,
    COUNT(transaction_id) AS txn_count,
    SUM(amount_inr) AS total_amount
FROM fact_transactions
WHERE transaction_type IN ('SIP', 'LUMPSUM')
GROUP BY age_group, transaction_type
ORDER BY age_group, txn_count DESC;

-- 8. Top 3 Fund Houses by Total AUM
SELECT 
    fund_house,
    SUM(aum_crore) as total_aum
FROM fact_performance
GROUP BY fund_house
ORDER BY total_aum DESC
LIMIT 3;

-- 9. Schemes with negative 1-year returns but positive 3-year returns (Turnaround funds)
SELECT 
    scheme_name,
    return_1yr_pct,
    return_3yr_pct
FROM fact_performance
WHERE return_1yr_pct < 0 AND return_3yr_pct > 0;

-- 10. Most popular payment mode for Redemptions
SELECT 
    payment_mode,
    COUNT(transaction_id) AS withdrawal_count,
    SUM(amount_inr) AS total_withdrawn
FROM fact_transactions
WHERE transaction_type = 'REDEMPTION'
GROUP BY payment_mode
ORDER BY total_withdrawn DESC;