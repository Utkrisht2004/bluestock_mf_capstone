# check_db.py
import sqlite3
import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "data", "db", "bluestock_mf.db")

try:
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Check total rows in the historical NAV table
    total_nav_rows = pd.read_sql_query("SELECT COUNT(*) as total_records FROM fact_nav", conn)
    print("--- Database Summary ---")
    print(f"Total NAV records stored: {total_nav_rows.iloc[0]['total_records']}")
    
    # 2. View the absolute latest entries across the portfolio
    print("\nMost Recent NAV Updates Captured:")
    latest_entries = pd.read_sql_query("""
        SELECT f.scheme_name, n.date, n.nav 
        FROM fact_nav n
        JOIN dim_fund f ON n.amfi_code = f.amfi_code
        ORDER BY n.date DESC, f.scheme_name ASC
        LIMIT 5
    """, conn)
    print(latest_entries.to_string(index=False))
    
    conn.close()
except Exception as e:
    print(f"❌ Error checking database: {e}")