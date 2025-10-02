import pandas as pd
import numpy as np

def load_data(file_path, ticker, start_date, end_date):
    df = pd.read_csv(file_path, parse_dates=["Date"])
    df = df[(df["Date"] >= pd.to_datetime("2007-01-01")) & (df["Date"] <= pd.to_datetime("2020-12-31"))]
    df = df[df["Symbol"].isin(ticker.split())]
    df = df.sort_values("Date").reset_index(drop=True)
    return df

def calculate_var(df, confidence_level, window, portfolio_value):
    df["Returns"] = df["Close"].pct_change().dropna()

    # Historical Simulation
    historical_var = df["Returns"].rolling(window).apply(
        lambda x: np.percentile(x, 100 - confidence_level), raw=True
    ) * portfolio_value
    historical_var = historical_var.abs()  # make positive

    # Parametric (Variance-Covariance)
    mu = df["Returns"].rolling(window).mean()
    sigma = df["Returns"].rolling(window).std()
    z_score = {90: 1.28, 95: 1.65, 99: 2.33}[confidence_level]
    parametric_var = (mu - z_score * sigma) * portfolio_value
    parametric_var = parametric_var.abs()  # make positive

    summary = {
        "Historical VaR (last)": historical_var.dropna().iloc[-1] if not historical_var.dropna().empty else None,
        "Parametric VaR (last)": parametric_var.dropna().iloc[-1] if not parametric_var.dropna().empty else None
    }

    return {
        "summary": summary,
        "historical_var": historical_var,
        "parametric_var": parametric_var
    }
