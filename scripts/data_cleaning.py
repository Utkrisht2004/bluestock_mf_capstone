import pandas as pd
import os

def clean_nav_history():
    raw_path = "data/raw/02_nav_history.csv"
    processed_path = "data/processed/02_nav_history.csv" 

    print("--- Day 2, Task 1: Cleaning NAV History ---")
    try:
        df = pd.read_csv(raw_path)
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['date'])
        df = df.drop_duplicates(subset=['amfi_code', 'date'])
        
        df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
        df = df[df['nav'] > 0]

        df = df.sort_values(by=['amfi_code', 'date'])
        df = df.set_index('date')
        df_cleaned = df.groupby('amfi_code')['nav'].resample('D').ffill().reset_index()

        os.makedirs("data/processed", exist_ok=True)
        df_cleaned.to_csv(processed_path, index=False)
        print(f"✅ Success: Cleaned NAV history saved to {processed_path}\n")

    except Exception as e:
        print(f"❌ Error in NAV cleaning: {e}\n")


def clean_transactions():
    raw_path = "data/raw/08_investor_transactions.csv"
    processed_path = "data/processed/08_investor_transactions.csv"

    print("--- Day 2, Task 2: Cleaning Investor Transactions ---")
    try:
        df = pd.read_csv(raw_path)
        print(f"Initial shape: {df.shape}")

        # 1. Fix date formats (Using 'transaction_date')
        print("Standardizing dates...")
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
        df = df.dropna(subset=['transaction_date'])

        # 2. Standardize transaction_type
        print("Standardizing transaction types...")
        df['transaction_type'] = df['transaction_type'].astype(str).str.strip().str.upper()
        
        type_mapping = {
            'SYSTEMATIC INVESTMENT PLAN': 'SIP',
            'LUMP SUM': 'LUMPSUM',
            'WITHDRAWAL': 'REDEMPTION'
        }
        df['transaction_type'] = df['transaction_type'].replace(type_mapping)
        
        allowed_types = ['SIP', 'LUMPSUM', 'REDEMPTION']
        invalid_types_count = len(df[~df['transaction_type'].isin(allowed_types)])
        if invalid_types_count > 0:
            print(f"  -> Dropped {invalid_types_count} rows with unknown transaction types.")
            df = df[df['transaction_type'].isin(allowed_types)]

        # 3. Validate amount > 0 (Using 'amount_inr')
        print("Validating transaction amounts...")
        df['amount_inr'] = pd.to_numeric(df['amount_inr'], errors='coerce')
        invalid_amounts = len(df[(df['amount_inr'] <= 0) | (df['amount_inr'].isna())])
        if invalid_amounts > 0:
            print(f"  -> Dropped {invalid_amounts} rows with invalid amounts (<= 0).")
        df = df[df['amount_inr'] > 0]

        # 4. Check and clean KYC status
        print("Checking KYC statuses...")
        if 'kyc_status' in df.columns:
            df['kyc_status'] = df['kyc_status'].astype(str).str.strip().str.title()
            allowed_kyc = ['Verified', 'Pending', 'Rejected']
            
            invalid_kyc_mask = ~df['kyc_status'].isin(allowed_kyc)
            invalid_kyc_count = invalid_kyc_mask.sum()
            
            if invalid_kyc_count > 0:
                print(f"  -> Found {invalid_kyc_count} rows with bad KYC status. Defaulting to 'Pending'.")
                df.loc[invalid_kyc_mask, 'kyc_status'] = 'Pending'

        # Save to processed directory
        os.makedirs("data/processed", exist_ok=True)
        df.to_csv(processed_path, index=False)
        
        print(f"Cleaned shape: {df.shape}")
        print(f"✅ Success: Cleaned transactions saved to {processed_path}\n")

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def clean_performance():
    raw_path = "data/raw/07_scheme_performance.csv"
    processed_path = "data/processed/07_scheme_performance.csv"

    print("--- Day 2, Task 3: Cleaning Scheme Performance ---")
    try:
        df = pd.read_csv(raw_path)
        print(f"Initial shape: {df.shape}")

        # 1. Validate all metric columns are numeric
        print("Validating numeric return values...")
        numeric_cols = [
            'return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 
            'benchmark_3yr_pct', 'alpha', 'beta', 'sharpe_ratio', 
            'sortino_ratio', 'std_dev_ann_pct', 'max_drawdown_pct', 
            'aum_crore', 'expense_ratio_pct'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                # errors='coerce' forces any letters/symbols into NaN (blank)
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # 2. Check Expense Ratio range (0.1% - 2.5%)
        print("Checking expense ratio bounds...")
        # First, drop rows where expense ratio is completely missing
        df = df.dropna(subset=['expense_ratio_pct'])
        
        invalid_er = len(df[(df['expense_ratio_pct'] < 0.1) | (df['expense_ratio_pct'] > 2.5)])
        if invalid_er > 0:
            print(f"  -> Dropped {invalid_er} funds outside the 0.1% - 2.5% expense ratio bounds.")
            df = df[(df['expense_ratio_pct'] >= 0.1) & (df['expense_ratio_pct'] <= 2.5)]

        # 3. Flag Anomalies
        print("Flagging performance anomalies...")
        # Let's flag anything with a 1-year return greater than 150% or less than -50%
        anomaly_mask = (df['return_1yr_pct'] > 150) | (df['return_1yr_pct'] < -50)
        anomaly_count = anomaly_mask.sum()
        
        if anomaly_count > 0:
            print(f"  -> ⚠️ WARNING: Found {anomaly_count} schemes with extreme 1-year returns (>150% or <-50%). Dropping them.")
            df = df[~anomaly_mask] # Keep only the rows that are NOT anomalies

        # Save to processed directory
        os.makedirs("data/processed", exist_ok=True)
        df.to_csv(processed_path, index=False)
        
        print(f"Cleaned shape: {df.shape}")
        print(f"✅ Success: Cleaned performance data saved to {processed_path}\n")

    except FileNotFoundError:
        print(f"❌ Error: Could not find {raw_path}.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Run all three cleaning tasks
    clean_nav_history()
    clean_transactions()
    clean_performance()