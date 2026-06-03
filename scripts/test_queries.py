import sqlite3
import pandas as pd
import os

def run_queries():
    db_path = "data/db/bluestock_mf.db"
    sql_path = "sql/queries.sql"

    print("=== Testing Analytical SQL Queries ===\n")
    
    if not os.path.exists(db_path):
        print(f"❌ Error: Database not found at {db_path}")
        return
        
    if not os.path.exists(sql_path):
        print(f"❌ Error: SQL file not found at {sql_path}")
        return

    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        
        # Read the SQL file
        with open(sql_path, 'r') as file:
            sql_script = file.read()
            
        # Split the script into individual queries based on the semicolon
        queries = sql_script.split(';')
        
        for query in queries:
            # Clean up whitespace
            query = query.strip()
            if not query:
                continue
                
            # Extract the comment to use as a title
            lines = query.split('\n')
            title = [line for line in lines if line.startswith('--')]
            sql_statement = '\n'.join([line for line in lines if not line.startswith('--')])
            
            # Print the title if it exists
            if title:
                print(f"\033[1;36m{title[-1]}\033[0m") # Prints title in cyan (if terminal supports it)
            
            # Execute and print the results using Pandas for pretty formatting
            if sql_statement.strip():
                try:
                    df = pd.read_sql_query(sql_statement, conn)
                    if df.empty:
                        print("  (No results found)")
                    else:
                        print(df.to_string(index=False)) # Hides the index numbers for cleaner output
                except Exception as e:
                    print(f"  ❌ Query Error: {e}")
            
            print("-" * 60 + "\n")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    run_queries()