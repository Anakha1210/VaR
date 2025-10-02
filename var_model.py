import pandas as pd
import numpy as np

def load_data(file_path, ticker, start_date, end_date):
    """Load CSV and filter by ticker + date range."""
    df = pd.read_csv(file_path, parse_dates=["Date"])
    df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]
    df = df[df["Symbol"].isin(ticker.split())]
    df = df.sort_values("Date").reset_index(drop=True)

    # Compute daily returns
    df["Returns"] = df["Close"].pct_change()
    return df


def calculate_var(df, confidence_level, window, portfolio_value):
    """Calculate Historical and Parametric VaR."""
    returns = df["Returns"].dropna()

    # -------- Historical Simulation --------
    historical_var = returns.rolling(window).apply(
        lambda x: np.percentile(x, 100 - confidence_level), raw=True
    ) * portfolio_value
    historical_var = historical_var.abs()  # ensure positive loss values

    # -------- Parametric (Variance-Covariance) --------
    mu = returns.rolling(window).mean()
    sigma = returns.rolling(window).std()
    z_score = {90: 1.28, 95: 1.65, 99: 2.33}[confidence_level]
    parametric_var = (mu - z_score * sigma) * portfolio_value
    parametric_var = parametric_var.abs()

    # -------- Output Summary --------
    summary = {
        "Historical VaR (last)": historical_var.dropna().iloc[-1] if not historical_var.dropna().empty else None,
        "Parametric VaR (last)": parametric_var.dropna().iloc[-1] if not parametric_var.dropna().empty else None
    }

    return {
        "summary": summary,
        "returns": returns,  # keep daily returns for histograms
        "historical_var": historical_var,
        "parametric_var": parametric_var
    }
