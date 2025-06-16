import streamlit as st
import pandas as pd
import ta
import yfinance as yf

st.set_page_config(page_title="Bilow Kherow Binary AI", layout="centered")

st.title("📈 Bilow Kherow Binary AI")
st.markdown("Get Smart Signals for 5s Expiry 🚀")

symbol = st.selectbox("Choose a currency pair", ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD"])
btn = st.button("🔮 Get 5s Signal")

def get_signal(symbol):
    data = yf.download(tickers=symbol + "=X", period="1d", interval="1m")
    if data is None or data.empty:
        return "No data available"

    df = data.copy()
    df['EMA9'] = ta.trend.ema_indicator(df['Close'], window=9)
    df['EMA21'] = ta.trend.ema_indicator(df['Close'], window=21)
    df['MACD'] = ta.trend.macd_diff(df['Close'])
    df['StochRSI'] = ta.momentum.stochrsi(df['Close'])

    latest = df.iloc[-1]
    signals = []

    if latest['EMA9'] > latest['EMA21']:
        signals.append("BUY")
    else:
        signals.append("SELL")

    if latest['MACD'] > 0:
        signals.append("BUY")
    else:
        signals.append("SELL")

    if latest['StochRSI'] < 0.2:
        signals.append("BUY")
    elif latest['StochRSI'] > 0.8:
        signals.append("SELL")

    if signals.count("BUY") >= 2:
        return "✅ BUY"
    elif signals.count("SELL") >= 2:
        return "❌ SELL"
    else:
        return "🤔 WAIT"

if btn:
    with st.spinner("Analyzing market..."):
        signal = get_signal(symbol)
        st.success(f"Signal for {symbol}: **{signal}**")
