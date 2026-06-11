import requests
import sqlite3
import pandas as pd
from datetime import datetime
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(SCRIPT_DIR, "..", "data", "db", "bluestock_mf.db")

API_BASE_URL = "https://api.mfapi.in/mf/"

def run_daily_etl():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Daily NAV ETL Pipeline...")
    
    try:
        # 1. Connect to Database and get our list of 40 active funds
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        df_funds = pd.read_sql_query("SELECT amfi_code, scheme_name FROM dim_fund", conn)
        active_funds = df_funds['amfi_code'].tolist()
        
        new_records_added = 0
        
        # 2. Loop through funds and fetch live data
        for amfi in active_funds:
            # Find the latest date we currently have in our database for this fund
            cursor.execute(f"SELECT MAX(date) FROM fact_nav WHERE amfi_code = '{amfi}'")
            latest_db_date_str = cursor.fetchone()[0]
            latest_db_date = datetime.strptime(latest_db_date_str, '%Y-%m-%d').date() if latest_db_date_str else None
            
            # Ping the live API
            response = requests.get(f"{API_BASE_URL}{amfi}")
            if response.status_code != 200:
                print(f"  ⚠️ Warning: API failed for {amfi}")
                continue
                
            data = response.json()
            if 'data' not in data or len(data['data']) == 0:
                continue
                
            # Grab the absolute latest NAV from the API
            latest_api_entry = data['data'][0]
            api_date = datetime.strptime(latest_api_entry['date'], '%d-%m-%Y').date()
            api_nav = float(latest_api_entry['nav'])
            
            # 3. Upsert Logic: Only insert if the API date is newer than our Database date
            if latest_db_date is None or api_date > latest_db_date:
                # Insert the new record
                insert_query = """
                    INSERT INTO fact_nav (amfi_code, date, nav) 
                    VALUES (?, ?, ?)
                """
                cursor.execute(insert_query, (amfi, api_date.strftime('%Y-%m-%d'), api_nav))
                new_records_added += 1
                print(f"  ✅ Added new NAV for {amfi}: {api_date} | ₹{api_nav}")
        
        # 4. Commit and Close
        conn.commit()
        conn.close()
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ETL Complete. {new_records_added} new daily records appended.")
        
    except Exception as e:
        print(f"❌ Critical ETL Failure: {e}")

if __name__ == "__main__":
    run_daily_etl()