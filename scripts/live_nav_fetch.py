import requests
import pandas as pd
import os
import time

def fetch_and_save_nav():
    """
    Fetches historical NAV data from mfapi.in for specified mutual funds
    and saves them as raw CSV files.
    """
    # The target funds and their AMFI scheme codes
    target_funds = {
        "HDFC_Top_100_Direct": 125497,
        "SBI_Bluechip": 119551,
        "ICICI_Bluechip": 120503,
        "Nippon_Large_Cap": 118632,
        "Axis_Bluechip": 119092,
        "Kotak_Bluechip": 120841
    }
    
    output_dir = "data/raw"
    
    print("Starting live NAV data extraction...\n" + "="*40)

    for fund_name, scheme_code in target_funds.items():
        print(f"Fetching data for {fund_name} (Code: {scheme_code})...")
        url = f"https://api.mfapi.in/mf/{scheme_code}"
        
        try:
            response = requests.get(url)
            response.raise_for_status() # Check for bad HTTP responses (4xx or 5xx)
            
            json_data = response.json()
            
            # The API returns a dictionary with 'meta' and 'data' keys. We want 'data'.
            if "data" in json_data and len(json_data["data"]) > 0:
                # Convert the list of dictionaries directly into a Pandas DataFrame
                df = pd.DataFrame(json_data["data"])
                
                # Add identifier columns so we don't lose track of which data is which
                df['scheme_code'] = scheme_code
                df['fund_name'] = fund_name
                
                # Reorder columns for readability
                df = df[['scheme_code', 'fund_name', 'date', 'nav']]
                
                # Save to CSV
                file_path = os.path.join(output_dir, f"{fund_name}_nav.csv")
                df.to_csv(file_path, index=False)
                
                print(f"  -> Success: Saved {len(df)} records to {file_path}")
            else:
                print(f"  -> Warning: No historical NAV data found for {fund_name}.")
                
        except requests.exceptions.RequestException as e:
            print(f"  -> Error: Failed to connect or fetch data for {fund_name}. Details: {e}")
            
        # Pause for 1 second between requests to be polite to the API server
        time.sleep(1)

    print("="*40 + "\nData extraction complete.")

if __name__ == "__main__":
    fetch_and_save_nav()