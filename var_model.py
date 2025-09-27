import pandas as pd
import numpy as np
from scipy.stats import norm

def get_asset_price(symbols):
    df=pd.read_csv("data/asset.csv",parse_dates=['data'])
    df=df[df['symbol'].isin(symbols)]
    df=df.pivot(index='date',columns='symbol',values='close_price')
    return df.sort_index()

def get_portfolio(portfolio_id):
    df=pd.read_csv('data/portfolio.csv')
    return df[df['portfolio_id']==Ticker]

def cal_potfolio_pnl(holdings_df,prices_df):
    pnl= (prices_df* holdingd_df.set_index('symbol')['quantity']).sum(axis=1)
    return pnl

def parametric_var(pnl,confidence):
    m=pnl.mean()
    sigma=pnl.std()
    z=norm.ppf(1-confidence)
    return -(m+z*sigma)

def historical_var(pnl,confidence):
    return -np.percentile(pnl,(1-confidence)*100)

def monte_carlo_var(pnl,confidence,simulations=10000):
    m=pnl.mean()
    sigma=pnl.std()
    sim_pnl=np.random.normal(m,sigma,simulations)
    return -np.percentile(sim_pnl,(1-confidence)*100)


def rolling_var(pnl,window,confidence):
    return pnl.rolling(window).apply(lambda x: -np.percentile(x,(1-confidence)*100))