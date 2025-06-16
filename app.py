import streamlit as st
import pandas as pd
import numpy as np
import ta
import yfinance as yf

st.set_page_config(page_title="Bilow Kherow Binary AI", layout="centered")

st.title("📉 Bilow Kherow Binary AI")
st.subheader("Smart 5-Second Signal Generator")

st.markdown("Tap the button below to get a real-time signal (BUY ✅ or SELL ❌) based on live market indicators.")

button = st.button("🕔 Get 5s Signal")

if button:
    st.info("Analyzing... Please wait 1–2 seconds.")
    
    # Get data from EUR/USD 1-minute chart (last 50 candles)
    df = yf.download("EURUSD=X", interval="1m", period="30m")
    df.dropna(inplace=True)

    # Apply indicators
    df['ema9'] = ta.trend.ema_indicator(df['Close'], window=9)
    df['ema21'] = ta.trend.ema_indicator(df['Close'], window=21)
    macd = ta.trend.macd_diff(df['Close'])
    stoch_rsi = ta.momentum.stochrsi_k(df['Close'])

    # Latest values
    latest_close = df['Close'].iloc[-1]
    ema9_latest = df['ema9'].iloc[-1]
    ema21_latest = df['ema21'].iloc[-1]
    macd_latest = macd.iloc[-1]
    stoch_latest = stoch_rsi.iloc[-1]

    # Signal logic
    confirmations = 0
    if ema9_latest > ema21_latest:
        confirmations += 1
    if macd_latest > 0:
        confirmations += 1
    if stoch_latest > 50:
        confirmations += 1

    # Final signal
    if confirmations >= 2:
        st.success("✅ Signal: BUY")
    else:
        st.error("❌ Signal: SELL")
