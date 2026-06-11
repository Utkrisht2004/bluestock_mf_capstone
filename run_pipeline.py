"""
Bluestock MF - Master Execution Pipeline
----------------------------------------
This script orchestrates the entire data lifecycle:
1. Daily NAV Data Extraction (ETL)
2. Quantitative Scoring & Risk Processing (Notebook Execution)
3. Automated Reporting & Alerting
"""

import os
import subprocess
import time
from datetime import datetime

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(SCRIPT_DIR, "venv", "Scripts", "python.exe") # Windows path

def log(message):
    """Simple logging utility."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

def run_script(script_path):
    """Executes a standard Python script."""
    try:
        log(f"Executing: {os.path.basename(script_path)}")
        # Using the virtual environment's python directly
        subprocess.run([VENV_PYTHON, script_path], check=True)
        log(f"✅ Success: {os.path.basename(script_path)}\n")
    except subprocess.CalledProcessError as e:
        log(f"❌ Failed to execute {os.path.basename(script_path)}. Error: {e}")
        raise

def run_notebook(notebook_path):
    """Executes a Jupyter Notebook headlessly."""
    try:
        log(f"Executing Notebook: {os.path.basename(notebook_path)}")
        subprocess.run([
            "jupyter", "nbconvert", "--to", "notebook", "--execute",
            "--inplace", notebook_path
        ], check=True)
        log(f"✅ Success: {os.path.basename(notebook_path)}\n")
    except subprocess.CalledProcessError as e:
        log(f"❌ Failed to execute notebook {os.path.basename(notebook_path)}. Error: {e}")
        raise

if __name__ == "__main__":
    print("====================================================")
    print("      BLUESTOCK MF QUANT PIPELINE ORCHESTRATOR      ")
    print("====================================================\n")
    start_time = time.time()
    
    try:
        # Step 1: Run the Daily ETL
        run_script(os.path.join(SCRIPT_DIR, "b1_daily_etl.py"))
        
        # Step 2: Execute the Advanced Analytics Notebook to refresh DataFrames
        # (Assuming your notebook is saved in the notebooks folder)
        advanced_analytics_nb = os.path.join(SCRIPT_DIR, "notebooks", "06_advanced_analytics.ipynb")
        if os.path.exists(advanced_analytics_nb):
            run_notebook(advanced_analytics_nb)
        else:
            log(f"⚠️ Skipping Notebook execution: {advanced_analytics_nb} not found.")

        # Step 3: Fire off the Weekly Email Report
        run_script(os.path.join(SCRIPT_DIR, "b5_email_report.py"))
        
        elapsed = time.time() - start_time
        print("====================================================")
        log(f"🎉 PIPELINE COMPLETED SUCCESSFULLY in {elapsed:.2f} seconds!")
        print("====================================================")
        
    except Exception as e:
        print("\n====================================================")
        log("🚨 PIPELINE HALTED DUE TO ERROR")
        print("====================================================")