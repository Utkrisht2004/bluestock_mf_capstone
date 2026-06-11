# app.py - Bluestock Mutual Fund Analytics Dashboard
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Bluestock Quant Dashboard",
    page_icon="📈",
    layout="wide"
)

# Bulletproof path resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "data", "db", "bluestock_mf.db")
PROCESSED_DIR = os.path.join(SCRIPT_DIR, "data", "processed")

@st.cache_data
def load_dashboard_data():
    """Loads fund metadata from DB and merges calculated metrics cleanly without duplicate column suffixes."""
    try:
        # 1. Connect to DB to get authoritative fund catalog
        conn = sqlite3.connect(DB_PATH)
        df_db_funds = pd.read_sql_query("SELECT amfi_code, scheme_name, category FROM dim_fund", conn)
        conn.close()
        
        # 2. Load calculated quant files
        df_scorecard = pd.read_csv(os.path.join(PROCESSED_DIR, "fund_scorecard.csv"))
        df_ab = pd.read_csv(os.path.join(PROCESSED_DIR, "alpha_beta.csv"))
        
        # Strip string keys to prevent white space mismatch
        df_db_funds['amfi_code'] = df_db_funds['amfi_code'].astype(str).str.strip()
        df_scorecard['amfi_code'] = df_scorecard['amfi_code'].astype(str).str.strip()
        df_ab['amfi_code'] = df_ab['amfi_code'].astype(str).str.strip()
        
        # 3. Prevent suffix collision: Drop duplicate risk/reward metrics from scorecard if they exist
        cols_to_drop_from_scorecard = [col for col in ['scheme_name', 'alpha', 'beta'] if col in df_scorecard.columns]
        df_scorecard_cleaned = df_scorecard.drop(columns=cols_to_drop_from_scorecard)
        
        # 4. Merge metrics together cleanly
        df_metrics = pd.merge(df_scorecard_cleaned, df_ab[['amfi_code', 'beta', 'alpha']], on='amfi_code', how='inner')
        
        # 5. Final merge with database metadata
        df_final = pd.merge(df_db_funds, df_metrics, on='amfi_code', how='inner')
        return df_final
        
    except Exception as e:
        st.error(f"Error compiling dashboard data context: {e}")
        return pd.DataFrame()

# Title banner
st.title("📈 Bluestock Mutual Fund Advanced Analytics Hub")
st.markdown("An institutional-grade quant interface replacing traditional BI tools with native Python execution.")
st.write("---")

df_funds = load_dashboard_data()

if df_funds.empty:
    st.warning("⚠️ High-performance scorecards or database not found. Ensure previous scripts ran successfully.")
else:
    # 2. Sidebar Controls
    st.sidebar.header("Filter Engine")
    categories = st.sidebar.multiselect(
        "Select Fund Category:",
        options=df_funds['category'].unique(),
        default=df_funds['category'].unique()
    )
    
    min_sharpe = st.sidebar.slider(
        "Minimum Sharpe Ratio Threshold:",
        float(df_funds['sharpe_ratio'].min()),
        float(df_funds['sharpe_ratio'].max()),
        0.0
    )
    
    # Filter dataset dynamically
    df_filtered = df_funds[
        (df_funds['category'].isin(categories)) & 
        (df_funds['sharpe_ratio'] >= min_sharpe)
    ]
    
    if df_filtered.empty:
        st.info("No funds match the selected filter thresholds.")
    else:
        # 3. Key Performance Indicators (KPIs)
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric(label="Funds Under Analysis", value=len(df_filtered))
        with kpi2:
            avg_cagr = df_filtered['cagr_3yr_pct'].mean()
            st.metric(label="Average 3-Yr CAGR", value=f"{avg_cagr:.2f}%" if not pd.isna(avg_cagr) else "N/A")
        with kpi3:
            top_perf = df_filtered.sort_values(by='composite_score', ascending=False).iloc[0]['scheme_name']
            st.metric(label="Top Composite Performer", value=top_perf[:25] + "..." if len(top_perf) > 25 else top_perf)
            
        st.write("---")
        
        # 4. Interactive Tabs Layout
        tab1, tab2 = st.tabs(["🏆 Performance Leaderboard", "🛡️ Volatility Metrics"])
        
        with tab1:
            st.subheader("Fund Performance Rankings (Sorted by Composite Score)")
            display_cols = ['scheme_name', 'category', 'cagr_3yr_pct', 'sharpe_ratio', 'composite_score']
            st.dataframe(df_filtered[display_cols].sort_values(by='composite_score', ascending=False), use_container_width=True, hide_index=True)
            
            # Interactive Plotly Chart
            st.subheader("Risk vs Reward Mapping")
            fig = px.scatter(
                df_filtered, 
                x='sharpe_ratio', 
                y='cagr_3yr_pct', 
                size='composite_score', 
                color='category',
                hover_name='scheme_name',
                labels={'sharpe_ratio': 'Sharpe Ratio (Risk-Adjusted)', 'cagr_3yr_pct': '3-Yr Annualized Return (%)'},
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            st.subheader("Volatility Analysis Dashboard")
            risk_cols = ['scheme_name', 'category', 'beta', 'alpha', 'sharpe_ratio']
            st.dataframe(df_filtered[risk_cols].sort_values(by='beta', ascending=True), use_container_width=True, hide_index=True)
            
            # Visualizing Alpha vs Beta
            st.subheader("Alpha Generation vs Systematic Risk (Beta)")
            fig_risk = px.bar(
                df_filtered.sort_values(by='alpha', ascending=False).head(10),
                x='scheme_name',
                y='alpha',
                color='beta',
                labels={'scheme_name': 'Fund Name', 'alpha': 'Alpha Score'},
                title="Top 10 Alpha Generating Funds vs Underlying Beta Profile",
                template="plotly_white"
            )
            st.plotly_chart(fig_risk, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Developed for Bluestock FinTech Capstone Program.")