import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
pip install streamlit

stock = "AAPL"
data = yf.download(stock, period="6mo")
data = data[['Close']]
data.dropna(inplace=True)

data.head()

data["MA20"]=data["Close"].rolling(20).mean()
data["MA50"]=data["Close"].rolling(50).mean()

current_price = data['Close'].iloc[-1]
ma20 = data['MA20'].iloc[-1]
ma50 = data['MA50'].iloc[-1]

if current_price.item() > ma20 > ma50:
    trend = "Strong Uptrend"
elif current_price.item() < ma20 < ma50:
    trend = "Strong Downtrend"
else:
    trend = "Mixed Trend"

print("Trend:", trend)

delta = data['Close'].diff()

gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()

rs = avg_gain / avg_loss

rsi = 100 - (100 / (1 + rs))

data['RSI_14'] = rsi

data.tail()

latest_rsi = data['RSI_14'].iloc[-1]
print("Latest RSI:", latest_rsi)

if latest_rsi > 70:
    print("Overbought → Possible Sell Signal")
elif latest_rsi < 30:
    print("Oversold → Possible Buy Signal")
else:
    print("Neutral")


data['Returns'] = data['Close'].pct_change()

vol_20 = data['Returns'].rolling(window=20).std()

annual_vol = vol_20 * np.sqrt(252)
data['Volatility_20d_annualized'] = annual_vol

latest_vol = data['Volatility_20d_annualized'].iloc[-1]
print("20-day Annualized Volatility:", latest_vol)

if latest_vol > 0.40:
    print("High Volatility (>40%)")
elif latest_vol >= 0.25:
    print("Medium Volatility (25%–40%)")
else:
    print("Low Volatility (<25%)")

Portfolio = {'AAPL':0.25,
             'MSFT':0.20,
             'JNJ':0.20,
             'JPM':0.15,
             'PG':0.20
}

end_date=pd.Timestamp.now()#normalize()to make 0
print(end_date)
start_date=end_date-pd.DateOffset(years=1)
print(start_date)

prices =pd.DataFrame()
prices.head()

for symbol in Portfolio:
  data = yf.download(symbol,
                     start = start_date,
                     end = end_date,
                     progress = False,
                     auto_adjust = True,
                     multi_level_index = False
  )
  prices[symbol] = data['Close']

  benchmark = yf.download("SPY",
                        start=start_date,
                        end=end_date,
                        progress=False,
                        auto_adjust = True)

benchmark = benchmark['Close']

prices.head()
benchmark.head()

daily_returns=prices.pct_change().dropna()
benchmark_returns=benchmark.pct_change().dropna()


daily_returns.head()

start_date = "2025-01-01"
end_date = "2026-01-01"

prices = pd.DataFrame()
for symbol in Portfolio:
    data = yf.download(symbol, start=start_date, end=end_date, progress=False, auto_adjust=True)
    prices[symbol] = data['Close']

common_index=daily_returns.index.intersection(benchmark_returns.index)

daily_returns=daily_returns.loc[common_index]
benchmark_returns=benchmark_returns.loc[common_index]

daily_returns.shape

portfolio_returns=pd.Series(0.0,index=daily_returns.index)
for symbol, weight in Portfolio.items():
    portfolio_returns+=weight*daily_returns[symbol]

portfolio_returns.head()

portfolio_total = (1 + portfolio_returns).prod() -1
benchmark_total = (1 + benchmark_returns).prod() -1

portfolio_vol = daily_returns.std() * np.sqrt(252)
benchmark_vol = benchmark_returns.std() * np.sqrt(252)

risk_free_rate = 0.03

portfolio_sharpe = (portfolio_total - risk_free_rate) / portfolio_vol
benchmark_sharpe = (benchmark_total - risk_free_rate) / benchmark_vol

print('PERFORMANCE DASHBOARD')
print('='*40)
print(f'Portfolio Return: {portfolio_total}')
print(f'Benchmark Return: {benchmark_total}')
print(f'Performance : {portfolio_total - benchmark_total}')
print(f'\n Portfolio Volatility : {portfolio_vol}')
print(f'Benchmark Volatility : {benchmark_vol}')
print(f'Portfolio Sharpe Ratio : {portfolio_sharpe}')
print(f'Benchmark Sharpe Ratio : {benchmark_sharpe}')

