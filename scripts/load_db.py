import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import os

def build_and_load_db():
    db_file = "data/db/bluestock_mf.db"
    db_uri = f"sqlite:///{db_file}"
    schema_file = "sql/schema.sql"
    
    print("--- Day 2, Tasks 4 & 5: Database Creation and Loading ---")
    
    # 1. Execute the SQL Schema to create the tables strictly
    print("1. Executing schema.sql to create Star Schema...")
    try:
        with sqlite3.connect(db_file) as conn:
            with open(schema_file, 'r') as f:
                schema_script = f.read()
            conn.executescript(schema_script)
        print("  -> Schema created successfully.")
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        return

    # 2. Connect with SQLAlchemy for Pandas bulk loading
    engine = create_engine(db_uri)
    
    # Dictionary mapping table names to their respective CSV files
    # Note: Using raw data for fund_master since we didn't explicitly clean it, 
    # but using processed data for the ones we cleaned today!
    datasets = {
        'dim_fund': 'data/raw/01_fund_master.csv',
        'fact_nav': 'data/processed/02_nav_history.csv',
        'fact_performance': 'data/processed/07_scheme_performance.csv',
        'fact_transactions': 'data/processed/08_investor_transactions.csv'
    }

    # 3. Load the data
    print("\n2. Pushing data to SQLite...")
    for table_name, csv_path in datasets.items():
        try:
            print(f"Loading {csv_path} into '{table_name}'...")
            df = pd.read_csv(csv_path)
            
            # Use if_exists='append' so we don't overwrite our strict schema definitions
            df.to_sql(table_name, con=engine, if_exists='append', index=False)
            
            # Verification step requested in your prompt
            print(f"  ✅ Success: Inserted {len(df)} rows into {table_name}")
            
        except FileNotFoundError:
            print(f"  ❌ Error: Could not find {csv_path}. Skipping.")
        except Exception as e:
            print(f"  ❌ Error loading {table_name}: {e}")

    print("\nDatabase build and load complete! Your bluestock_mf.db is ready.")

if __name__ == "__main__":
    build_and_load_db()