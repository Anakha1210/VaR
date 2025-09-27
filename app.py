import streamlit as st
import pandas as pd
from var_model import get_portfolio, get_asset_price, cal_potfolio_pnl, parametric_var, historical_var, monte_carlo_var

st.title("📊 Value at Risk Calculator")
st.sidebar.header("Portfolio Inputs")


tickers_input = st.sidebar.text_input("Enter tickers separated by space", "RELIANCE TCS INFY HDFCBANK ICICIBANK")
tickers = tickers_input.split()

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-12-31"))

rolling_window = st.sidebar.number_input("Rolling Window (days)", value=252, min_value=1, step=1)

confidence_level = st.sidebar.slider("Confidence Level", 0.0, 1.0, 0.95)

portfolio_value = st.sidebar.number_input("Portfolio Value (₹)", value=1000000, step=10000)

portfolio_id = 1  

simulations = st.sidebar.number_input("Monte Carlo Simulations", value=10000, step=1000)


if st.button("Calculate VaR"):
    
    portfolio_df = get_portfolio(portfolio_id)
    symbols = portfolio_df['symbol'].tolist()
    prices_df = get_asset_price(symbols)
    
    
    prices_df = prices_df.loc[start_date:end_date]
    
    if prices_df.empty:
        st.warning("No data available for the selected tickers or date range.")
    else:
       
        pnl = cal_potfolio_pnl(portfolio_df, prices_df)
        
       
        param_var = parametric_var(pnl, confidence_level)
        hist_var = historical_var(pnl, confidence_level)
        mc_var = monte_carlo_var(pnl, confidence_level, simulations)
        
        
        st.subheader("📈 Portfolio Value at Risk (VaR)")
        st.write(f"**Parametric VaR:** ₹{param_var:,.2f}")
        st.write(f"**Historical VaR:** ₹{hist_var:,.2f}")
        st.write(f"**Monte Carlo VaR:** ₹{mc_var:,.2f}")
        
        st.subheader("📊 Portfolio PnL Distribution")
        st.line_chart(pnl)
