import pandas as pd
import numpy as np
from scipy.stats import norm

def get_asset_price(symbols):
    # The Date is already the index in asset.csv, so we don't need to set it again
    df = pd.read_csv("data/asset.csv", index_col='Date', parse_dates=True)
    # Return only the columns for the requested symbols
    return df[symbols]

def get_portfolio(portfolio_id=None):
    # portfolio_id parameter is not used in the current implementation
    # as portfolio.csv contains all tickers and weights
    df = pd.read_csv('data/portfolio.csv')
    return df

def cal_potfolio_pnl(holdings_df, prices_df):
    # Calculate daily returns
    returns = prices_df.pct_change().dropna()
    
    # Calculate weighted returns using portfolio weights
    weighted_returns = returns.mul(holdings_df['Weight'].values, axis=1)
    
    # Sum across all assets to get portfolio returns
    portfolio_returns = weighted_returns.sum(axis=1)
    
    return portfolio_returns

def parametric_var(pnl, confidence):
    m = pnl.mean()
    sigma = pnl.std()
    z = norm.ppf(1-confidence)
    return -(m+z*sigma)

def historical_var(pnl, confidence):
    return -np.percentile(pnl, (1-confidence)*100)

def monte_carlo_var(pnl, confidence, simulations=10000):
    m = pnl.mean()
    sigma = pnl.std()
    sim_pnl = np.random.normal(m, sigma, simulations)
    return -np.percentile(sim_pnl, (1-confidence)*100)

def rolling_var(pnl, window, confidence):
    return pnl.rolling(window).apply(lambda x: -np.percentile(x, (1-confidence)*100))