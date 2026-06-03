import pandas as pd
import glob
import os

def inspect_raw_data(data_path="data/raw"):
    """
    Loads all CSV files from the specified directory and prints their shape,
    data types, and first 5 rows.
    """
    # Find all CSV files in the data/raw folder
    csv_files = glob.glob(os.path.join(data_path, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {data_path}. Please place your datasets there first.")
        return None

    print(f"Found {len(csv_files)} CSV files. Beginning inspection...\n")
    print("=" * 50)
    
    # Dictionary to store dataframes if you want to use them later in the script
    dataframes = {}

    for file in csv_files:
        file_name = os.path.basename(file)
        print(f"--- Inspecting: {file_name} ---")
        
        try:
            # Load the dataset
            df = pd.read_csv(file)
            dataframes[file_name] = df
            
            # Print metrics
            print(f"Shape: {df.shape}")
            print("\nData Types:")
            print(df.dtypes)
            print("\nHead:")
            print(df.head())
            
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
            
        print("=" * 50 + "\n")
        
    return dataframes

if __name__ == "__main__":
    datasets = inspect_raw_data()
    print("Data ingestion and initial inspection complete.")