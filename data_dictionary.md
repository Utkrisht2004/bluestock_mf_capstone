# Mutual Fund Capstone: Data Dictionary

## Overview
This document defines the tables, columns, data types, and business logic for the `bluestock_mf.db` SQLite database. The database follows a Star Schema design.

---

## Dimension Table: `dim_fund`
Master list of all mutual fund schemes, providing categorical and structural details.

| Column Name | Data Type | Business Definition |
| :--- | :--- | :--- |
| `amfi_code` | INTEGER (PK) | Unique identifier assigned by the Association of Mutual Funds in India (AMFI). |
| `fund_house` | TEXT | The Asset Management Company (AMC) managing the fund. |
| `scheme_name` | TEXT | The official marketing name of the mutual fund scheme. |
| `category` | TEXT | High-level classification (e.g., Equity, Debt, Hybrid). |
| `sub_category` | TEXT | Specific investment mandate (e.g., Large Cap, Small Cap, Liquid). |
| `plan` | TEXT | Investment plan type (Direct vs. Regular). |
| `launch_date` | TEXT | The inception date of the fund. |
| `benchmark` | TEXT | The market index the fund's performance is measured against. |
| `expense_ratio_pct` | REAL | The annual maintenance charge levied by the fund (bounded 0.1% - 2.5%). |
| `exit_load_pct` | REAL | Penalty percentage applied if units are redeemed before a specific timeframe. |
| `risk_category` | TEXT | Standardized risk assessment (e.g., Low, Moderate, Very High). |

---

## Fact Table: `fact_nav`
Daily Net Asset Value (NAV) history for mutual funds. Weekends and holidays are mathematically forward-filled.

| Column Name | Data Type | Business Definition |
| :--- | :--- | :--- |
| `amfi_code` | INTEGER (FK) | Links to `dim_fund.amfi_code`. |
| `date` | TEXT | The trading date (YYYY-MM-DD). |
| `nav` | REAL | The Net Asset Value per unit at the end of the trading day. Validated strictly > 0. |

---

## Fact Table: `fact_transactions`
Record of individual investor transactions (inflows and outflows).

| Column Name | Data Type | Business Definition |
| :--- | :--- | :--- |
| `transaction_id` | INTEGER (PK) | Auto-incrementing unique identifier for the transaction. |
| `investor_id` | INTEGER | Unique identifier for the individual investor. |
| `transaction_date` | TEXT | The date the transaction was executed. |
| `amfi_code` | INTEGER (FK) | Links to `dim_fund.amfi_code`. |
| `transaction_type` | TEXT | Standardized ENUM: 'SIP', 'LUMPSUM', or 'REDEMPTION'. |
| `amount_inr` | REAL | The monetary value of the transaction in Indian Rupees. Validated strictly > 0. |
| `state` / `city` | TEXT | Geographic location of the investor. |
| `age_group` | TEXT | Demographic age bracket of the investor. |
| `kyc_status` | TEXT | Know Your Customer verification status (Verified, Pending, Rejected). |

---

## Fact Table: `fact_performance`
Calculated financial metrics, risk ratios, and total assets for the mutual funds.

| Column Name | Data Type | Business Definition |
| :--- | :--- | :--- |
| `amfi_code` | INTEGER (PK) | Links to `dim_fund.amfi_code`. |
| `return_1yr_pct` | REAL | Trailing 1-year percentage return. |
| `alpha` | REAL | The excess return of the fund relative to the return of the benchmark index. |
| `beta` | REAL | Measure of the fund's volatility in relation to the market. |
| `sharpe_ratio` | REAL | Risk-adjusted return calculation. |
| `aum_crore` | REAL | Assets Under Management expressed in Crores (INR). |
| `morningstar_rating` | REAL | Third-party quality rating (1 to 5 stars). |