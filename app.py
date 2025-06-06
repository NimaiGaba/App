import streamlit as st
import yfinance as yf
import ta
import pandas as pd

# App Title
st.title("📈 Stock Screener App")

# Sidebar Filters
st.sidebar.header("Filter Stocks")

# Stock input
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, INFY.NS)", value="AAPL")

# Date range (for now fixed period)
period = st.sidebar.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)

# Technical Filters
st.sidebar.subheader("Technical Filters")
rsi_min, rsi_max = st.sidebar.slider("RSI Range", 0, 100, (20, 80))
sma_window = st.sidebar.slider("SMA Window", 5, 50, 20)
show_macd = st.sidebar.checkbox("Show MACD", value=True)

if st.sidebar.button("Run Screener"):
    # Clean ticker input to get only one ticker (first token)
    ticker_clean = ticker.strip().split()[0].split(',')[0].upper()

    st.write(f"Showing results for {ticker_clean} - Period: {period}")

    # Fetch stock data
    data = yf.download(ticker_clean, period=period, interval='1d')

    # Check if data has multi-index columns (multi-ticker case)
    if isinstance(data.columns, pd.MultiIndex):
        # Extract close price series for the ticker
        close_series = data['Close'][ticker_clean]
    else:
        close_series = data['Close']

    st.write("Raw Data", data.tail())

    # Calculate indicators based on close_series
    data['SMA'] = ta.trend.sma_indicator(close_series, window=sma_window)
    data['RSI'] = ta.momentum.rsi(close_series, window=14)
    if show_macd:
        data['MACD'] = ta.trend.macd(close_series)

    # Prepare DataFrame for plotting Price & SMA
    if isinstance(data.columns, pd.MultiIndex):
        # Create DataFrame with Close and SMA columns for plotting
        plot_data = pd.DataFrame({
            'Close': close_series,
            'SMA': data['SMA']
        })
    else:
        plot_data = data[['Close', 'SMA']]

    st.subheader("Price & Moving Average")
    st.line_chart(plot_data)

    st.subheader("RSI")
    st.line_chart(data['RSI'])

    if show_macd:
        st.subheader("MACD")
        st.line_chart(data['MACD'])

# Watchlist Placeholder
st.subheader("📋 Watchlist")
st.info("Watchlist feature coming soon! (Week 2)")
