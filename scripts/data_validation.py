import pandas as pd
import os

def explore_and_validate():
    raw_dir = "data/raw"
    fund_master_path = os.path.join(raw_dir, "01_fund_master.csv")
    nav_history_path = os.path.join(raw_dir, "02_nav_history.csv")

    print("--- Step 5: Exploring Fund Master ---")
    try:
        fund_master = pd.read_csv(fund_master_path)
        
        print("\nUnique Fund Houses:")
        print(fund_master['fund_house'].nunique(), "houses found.")
        
        print("\nCategories:")
        print(fund_master['category'].unique())
        
        print("\nSub-Categories:")
        print(fund_master['sub_category'].unique())
        
        print("\nRisk Categories:")
        if 'risk_category' in fund_master.columns:
            print(fund_master['risk_category'].unique())
        else:
            print("Column 'risk_category' not found. Check column names.")
            
    except FileNotFoundError:
        print(f"Error: {fund_master_path} not found. Check if the file is in the data/raw folder.")
        return

    print("\n--- Step 6: Validating AMFI Codes ---")
    try:
        nav_history = pd.read_csv(nav_history_path)
        
        # Both datasets use 'amfi_code' now
        master_codes = set(fund_master['amfi_code'].dropna().astype(int))
        nav_codes = set(nav_history['amfi_code'].dropna().astype(int))
        
        # Find overlaps and missing codes
        missing_in_nav = master_codes - nav_codes
        missing_in_master = nav_codes - master_codes
        
        print("\nData Quality Summary:")
        print(f"Total unique schemes in Fund Master: {len(master_codes)}")
        print(f"Total unique schemes in NAV History: {len(nav_codes)}")
        
        if len(missing_in_nav) == 0:
            print("✅ SUCCESS: Every code in fund_master exists in nav_history.")
        else:
            print(f"⚠️ WARNING: {len(missing_in_nav)} codes in fund_master are MISSING from nav_history.")
            print(f"Sample of missing codes: {list(missing_in_nav)[:5]}")
            
        if len(missing_in_master) > 0:
            print(f"⚠️ WARNING: {len(missing_in_master)} codes in nav_history are MISSING from fund_master (Orphaned NAV data).")
            
    except FileNotFoundError:
        print(f"Error: {nav_history_path} not found. Check if the file is in the data/raw folder.")
    except KeyError as e:
        print(f"Error: Column {e} not found in the NAV dataset. Please verify the column name.")

if __name__ == "__main__":
    explore_and_validate()