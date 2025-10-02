import streamlit as st
import pandas as pd
from var_model import calculate_var, load_data
import os

HISTORY_FILE = "history.csv"

st.set_page_config(page_title="VaR Calculator", layout="wide")
st.title("📊 Value at Risk (VaR) Calculator")

# --- Sidebar Inputs ---
st.sidebar.header("Input Parameters")

tickers = st.sidebar.text_input("Enter Tickers (space-separated)", "MUNDRAPORT")

start_year = st.sidebar.selectbox("Start Year", list(range(2000, 2021)), index=7)  # default 2007
end_year = st.sidebar.selectbox("End Year", list(range(2000, 2021)), index=20)     # default 2020

rolling_window = st.sidebar.number_input("Rolling Window (days)", min_value=1, value=30)
confidence_level = st.sidebar.slider("Confidence Level (%)", 90, 99, 95)
portfolio_value = st.sidebar.number_input("Portfolio Value", min_value=1000, value=100000)

run_btn = st.sidebar.button("Calculate VaR")

# Convert years to datetime
start_date = pd.to_datetime(f"{start_year}-01-01")
end_date = pd.to_datetime(f"{end_year}-12-31")

# --- Run Calculation ---
if run_btn:
    df = load_data("data/NIFTY50/NIFTY50_all.csv", tickers, start_date, end_date)
    
    if df.empty:
        st.error("No data available for the selected ticker(s) and year range.")
    else:
        results = calculate_var(df, confidence_level, rolling_window, portfolio_value)

        # Input Summary Table
        st.subheader("Input Summary")
        summary_df = pd.DataFrame({
            "Parameter": ["Tickers", "Start Year", "End Year", "Rolling Window", "Confidence Level", "Portfolio Value"],
            "Value": [tickers, start_year, end_year, rolling_window, confidence_level, portfolio_value]
        })
        st.table(summary_df)

        # VaR Results
        st.subheader("VaR Results")
        var_results_df = pd.DataFrame({
            "Method": ["Historical VaR", "Parametric VaR"],
            "Value": [results["summary"]["Historical VaR (last)"], results["summary"]["Parametric VaR (last)"]]
        })
        st.table(var_results_df)

        # Charts
        st.subheader("Historical VaR Chart")
        st.line_chart(results["historical_var"])
        st.subheader("Parametric VaR Chart")
        st.line_chart(results["parametric_var"])

        # Save to history
        new_record = {
            "Tickers": tickers,
            "Start": start_date,
            "End": end_date,
            "Confidence": confidence_level,
            "Window": rolling_window,
            "Portfolio": portfolio_value,
            "Parametric VaR": results["summary"]["Parametric VaR (last)"],
            "Historical VaR": results["summary"]["Historical VaR (last)"]
        }
        history_df = pd.DataFrame([new_record])
        if os.path.exists(HISTORY_FILE):
            old = pd.read_csv(HISTORY_FILE)
            history_df = pd.concat([old, history_df]).tail(10)
        history_df.to_csv(HISTORY_FILE, index=False)

# --- History Section ---
if os.path.exists(HISTORY_FILE):
    st.subheader("📜 Last 10 Calculations")
    hist = pd.read_csv(HISTORY_FILE)
    st.table(hist.tail(10))
