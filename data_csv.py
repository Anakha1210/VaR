import pandas as pd

# Load full dataset
df = pd.read_csv("data/NIFTY50/NIFTY50_all.csv", parse_dates=["Date"])

# Choose tickers you want
tickers = ["ADANIPORTS","ASIANPAINT","AXISBANK","BAJAJ-AUTO","BAJAJFINSV","BAJAJFINANCE","BHARTIARTL","BPCL","BRITANNIA","CIPLA",
           "COALINDIA","DRREDDY","EICHERMOT","GAIL","GRASIM","HCLTECH","HDFC","HDFCBANK","HEROMOTOCO","HINDALCO","HINDUNILVR",
           "ICICIBANK","INDUSINDBK","INFRATEL","INFY","IOC","ITC","JSWSTEEL","KOTAKBANK","LT","MM","MARUTI","NESTLEIND","NTPC","ONGC",
           "POWERGRID","RELIANCE","SBIN","SHREECEM","SUNPHARMA","TATAMOTORS","TATASTEEL","TCS","TECHM","ULTRACEMCO","TITAN","UPL","WIPRO","VEDL","ZEEL" 
           ] 

# Filter only needed tickers
df = df[df["Symbol"].isin(tickers)]

# Pivot table: Dates as rows, tickers as columns, Close as values
df_asset = df.pivot(index="Date", columns="Symbol", values="Close")

# Sort by Date and forward fill missing values
df_asset = df_asset.sort_index().fillna(method="ffill")

# Save as asset.csv
df_asset.to_csv("data/asset.csv")
print("✅ Saved data/asset.csv with shape:", df_asset.shape)

weights = [1/len(tickers)]*len(tickers)
df_portfolio = pd.DataFrame({"Ticker": tickers, "Weight": weights})
df_portfolio.to_csv("data/portfolio.csv", index=False)
print("✅ portfolio.csv created with 30 tickers")