import streamlit as st
import pandas as pd
from var_model import calculate_var, load_data
import os

HISTORY_FILE = "history.csv"

st.set_page_config(page_title="VaR Calculator", layout="wide")
st.title("📊 Value at Risk (VaR) Calculator")

# --- Input Section ---
with st.form("var_form"):
    tickers = st.text_input("Enter Tickers (space-separated)", "MUNDRAPORT")
    
    # Year selection instead of free date
    start_year = st.selectbox("Start Year", list(range(2000, 2021)), index=7)  # default 2007
    end_year = st.selectbox("End Year", list(range(2000, 2021)), index=20)     # default 2020

    rolling_window = st.number_input("Rolling Window (days)", min_value=1, value=30)
    confidence_level = st.slider("Confidence Level (%)", 90, 99, 95)
    portfolio_value = st.number_input("Portfolio Value", min_value=1000, value=100000)

    submitted = st.form_submit_button("Calculate VaR")

if submitted:
    # Convert years to datetime
    start_date = pd.to_datetime(f"{start_year}-01-01")
    end_date = pd.to_datetime(f"{end_year}-12-31")

    df = load_data("data/data.csv", tickers, start_date, end_date)
    
    if df.empty:
        st.error("No data available for the selected ticker(s) and year range.")
    else:
        results = calculate_var(df, confidence_level, rolling_window, portfolio_value)

        # Display input summary
        st.subheader("Input Summary")
        st.write({
            "Tickers": tickers,
            "Start Year": start_year,
            "End Year": end_year,
            "Rolling Window": rolling_window,
            "Confidence Level": confidence_level,
            "Portfolio Value": portfolio_value
        })

        # Display VaR results
        st.subheader("VaR Results")
        st.write(results["summary"])

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

# History display
if os.path.exists(HISTORY_FILE):
    st.subheader("📜 Last 10 Calculations")
    hist = pd.read_csv(HISTORY_FILE)
    st.table(hist.tail(10))
