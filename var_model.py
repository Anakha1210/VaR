import pandas as pd
import numpy as np

def load_data(file_path, ticker, start_date, end_date):
    """
    Load and filter CSV data for a given ticker and date range.
    Filters the Kaggle NIFTY50 dataset for 2007-2020 if desired.
    """
    df = pd.read_csv(file_path, parse_dates=["Date"])
    
    # Keep only the requested date range
    df = df[(df["Date"] >= pd.to_datetime("2007-01-01")) & (df["Date"] <= pd.to_datetime("2020-12-31"))]

    # Filter for the selected ticker(s)
    df = df[df["Symbol"].isin(ticker.split())]

    # Sort by date
    df = df.sort_values("Date").reset_index(drop=True)
    
    return df

def calculate_var(df, confidence_level, window, portfolio_value):
    """Calculate Historical and Parametric VaR"""
    df["Returns"] = df["Close"].pct_change().dropna()

    # Historical Simulation
    historical_var = df["Returns"].rolling(window).apply(
        lambda x: np.percentile(x, 100 - confidence_level), raw=True
    ) * portfolio_value

    # Parametric (Variance-Covariance)
    mu = df["Returns"].rolling(window).mean()
    sigma = df["Returns"].rolling(window).std()
    z_score = {90: 1.28, 95: 1.65, 99: 2.33}[confidence_level]
    parametric_var = (mu - z_score * sigma) * portfolio_value

    summary = {
        "Historical VaR (last)": historical_var.dropna().iloc[-1] if not historical_var.dropna().empty else None,
        "Parametric VaR (last)": parametric_var.dropna().iloc[-1] if not parametric_var.dropna().empty else None
    }

    return {
        "summary": summary,
        "historical_var": historical_var,
        "parametric_var": parametric_var
    }
