# 📈 Bluestock Mutual Fund Quant Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Project Overview
This repository contains an end-to-end quantitative data pipeline and analytics dashboard built for the **Bluestock FinTech Capstone Program**. It transitions raw, scraped mutual fund data into institutional-grade financial metrics, automating the extraction, transformation, risk-modeling, and reporting processes.

Instead of relying on static spreadsheets or commercial BI tools, this project leverages a native Python ecosystem to handle stochastic simulations, portfolio optimization, and an interactive frontend interface.

## ✨ Key Features
* **Automated Daily ETL:** A scheduled pipeline (`b1_daily_etl.py`) that fetches live end-of-day NAV data from the `mfapi.in` API and performs logical upserts into a local SQLite database.
* **Quantitative Risk Engine:** Calculates advanced asset metrics including Sharpe Ratio, Alpha, Beta, Value at Risk (VaR 95%), Expected Shortfall (CVaR), and portfolio concentration (Herfindahl-Hirschman Index).
* **Stochastic Forecasting:** Implements Geometric Brownian Motion (GBM) Monte Carlo simulations to project 5-year NAV trajectories with 90% confidence bands.
* **Modern Portfolio Theory (MPT):** Utilizes `scipy.optimize` to map the Markowitz Efficient Frontier, mathematically identifying the Maximum Sharpe (Tangency) and Global Minimum Variance portfolios.
* **Interactive Web App:** A dynamic `Streamlit` dashboard (`app.py`) for live risk-reward visualization and fund filtering.
* **Automated Alerting:** A DevOps-ready script (`b5_email_report.py`) that compiles top algorithmic rankings into a responsive HTML template and transmits it via SMTP.

## 🏗️ Architecture & Tech Stack
* **Database:** `SQLite3` (Star-schema data warehouse for transactional and historical NAV data)
* **Data Processing & Quant Logic:** `Pandas`, `NumPy`, `SciPy`
* **Visualization:** `Matplotlib`, `Seaborn`, `Plotly Express`
* **Frontend:** `Streamlit`
* **Pipeline Orchestration:** Python `subprocess` & OS scripting

## 📂 Repository Structure
```text
bluestock_mf_capstone/
│
├── data/
│   ├── db/                 # SQLite database files (bluestock_mf.db)
│   ├── raw/                # Original scraped CSVs
│   └── processed/          # Cleaned scorecards and calculated metrics
│
├── notebooks/
│   └── 06_advanced_analytics.ipynb  # Core quantitative research and modeling
│
├── reports/
│   └── charts/             # Output directory for exported visualizations
|
|── scripts/                # Scripts for data ingestion
│
|── sql/                    # SQL Schema and files
|
├── app.py                  # Streamlit interactive dashboard
├── b1_daily_etl.py         # Live API extraction script
├── b5_email_report.py      # Automated HTML email engine
├── run_pipeline.py         # Master orchestrator script
├── requirements.txt        # Dependency mapping
└── README.md
```

## 🚀 Setup & Intsallation
* Clone the Repository
```
git clone [https://github.com/yourusername/bluestock_mf_capstone.git](https://github.com/yourusername/bluestock_mf_capstone.git)
cd bluestock_mf_capstone
```
* Environment Configuration
```
# Create the environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac/Linux:
source venv/bin/activate
```
* Install Dependencies
```
pip install -r requirements.txt
```
* Database Initialization
```
# Verify the database path
ls data/db/bluestock_mf.db
```

## ⚙️ Usage Instructions

* Running the Full Automated Pipeline
```
python run_pipeline.py
```
* Launching dashboard
```
streamlit run app.py
```

## 📊 Dataset Description

The internal SQLite database (bluestock_mf.db) contains several core tables:

* dim_fund: Master catalog of 40 selected mutual funds, including category and AMFI codes.

* fact_nav: Historical daily Net Asset Value (NAV) records for time-series analysis.

* investor_transactions: Granular ledger of retail SIP and lumpsum capital flows.

* benchmark_indices: Macro market tracking data (e.g., Nifty 50) for baseline comparisons.