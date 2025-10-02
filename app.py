import streamlit as st
import pandas as pd
from var_model import load_data, calculate_var
import matplotlib.pyplot as plt

st.set_page_config(page_title="VaR Calculator", layout="wide")

# ---------------- Sidebar Inputs ----------------
st.sidebar.header("User Inputs")

tickers = st.sidebar.text_input("Enter space-separated tickers", "MUNDRAPORT")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2007-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2020-12-31"))
window = st.sidebar.slider("Rolling Window (days)", 1, 252, 20)
confidence_level = st.sidebar.selectbox("Confidence Level (%)", [90, 95, 99], index=1)
portfolio_value = st.sidebar.number_input("Portfolio Value (INR)", min_value=10000, value=1000000, step=10000)

# ---------------- Load Data ----------------
df = load_data("data/NIFTY50/NIFTY50_all.csv", tickers, start_date, end_date)

if df.empty:
    st.error("No data found for the given inputs.")
    st.stop()

# ---------------- Input Summary ----------------
st.subheader("Input Summary")
summary_df = pd.DataFrame({
    "Tickers": [tickers],
    "Start Date": [start_date],
    "End Date": [end_date],
    "Rolling Window": [window],
    "Confidence Level": [confidence_level],
    "Portfolio Value (INR)": [portfolio_value]
})
st.table(summary_df)

# ---------------- Run Calculation ----------------
if st.button("Run Calculation"):
    results = calculate_var(df, confidence_level, window, portfolio_value)

    st.subheader("VaR Results (Last Value)")
    st.write(results["summary"])

    # ---------------- Time Series Charts ----------------
    st.subheader("VaR Time Series Charts")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Historical VaR")
        st.bar_chart(results["historical_var"])
    with col2:
        st.subheader("Parametric VaR")
        st.bar_chart(results["parametric_var"])

    # ---------------- Histograms with VaR Line ----------------
    def plot_var_histogram(returns, var_value, confidence_level, method_name, portfolio_value):
        scaled_returns = returns * portfolio_value
        scaled_returns = scaled_returns.dropna()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(scaled_returns, bins=50, color="skyblue", edgecolor="black", alpha=0.7)

        ax.axvline(-var_value, color="red", linestyle="--", linewidth=2,
                   label=f"VaR {confidence_level}%: -₹{var_value:,.2f}")

        ax.set_title(f"{method_name} VaR Histogram ({confidence_level}% confidence)")
        ax.set_xlabel("Portfolio Returns (INR)")
        ax.set_ylabel("Frequency")
        ax.legend()

        ax.text(-var_value, ax.get_ylim()[1]*0.8, f"-₹{var_value:,.2f}", color="red")

        st.pyplot(fig)

    st.subheader("VaR Histograms")

    col1, col2 = st.columns(2)

    with col1:
        if results["summary"]["Historical VaR (last)"] is not None:
            plot_var_histogram(
                df["Returns"].rolling(window).mean(),
                results["summary"]["Historical VaR (last)"],
                confidence_level,
                "Historical",
                portfolio_value
            )

    with col2:
        if results["summary"]["Parametric VaR (last)"] is not None:
            plot_var_histogram(
                df["Returns"],
                results["summary"]["Parametric VaR (last)"],
                confidence_level,
                "Parametric",
                portfolio_value
            )
