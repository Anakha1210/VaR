import streamlit as st
import pandas as pd
from var_model import calculate_var, load_data
import os

# File to store history
HISTORY_FILE = "history.csv"

st.set_page_config(page_title="VaR Calculator", layout="wide")

st.title("📊 Value at Risk (VaR) Calculator")

# --- Input Section ---
with st.form("var_form"):
    tickers = st.text_input("Enter Tickers (space-separated)", "MUNDRAPORT")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    rolling_window = st.number_input("Rolling Window (days)", min_value=1, value=30)
    confidence_level = st.slider("Confidence Level (%)", 90, 99, 95)
    portfolio_value = st.number_input("Portfolio Value", min_value=1000, value=100000)

    submitted = st.form_submit_button("Calculate VaR")

if submitted:
    # Load data from data folder
    df = load_data("data/NIFTY50/NIFTY50_all.csv", tickers, start_date, end_date)
    
    if df.empty:
        st.error("No data available for given filters.")
    else:
        # Calculate VaR
        results = calculate_var(df, confidence_level, rolling_window, portfolio_value)

        # Show Summary
        st.subheader("Input Summary")
        st.write({
            "Tickers": tickers,
            "Start Date": start_date,
            "End Date": end_date,
            "Rolling Window": rolling_window,
            "Confidence Level": confidence_level,
            "Portfolio Value": portfolio_value
        })

        st.subheader("VaR Results")
        st.write(results["summary"])

        # Plot Charts
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
