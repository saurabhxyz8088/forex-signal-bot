
import yfinance as yf
import pandas_ta as ta
import requests
import time
from datetime import datetime

# --- CONFIG ---
TELEGRAM_BOT_TOKEN = "8371622493:AAGjZexKllY722Pm9eNW30X8-hDGrQcbpOo"
TELEGRAM_CHAT_ID = "6504690145"
PAIR = "EURUSD=X"
INTERVAL = "5m"
PERIOD = "1d"
SLEEP_TIME = 300  # 5 minutes

def send_signal(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    print(f"Sent signal: {message}")

def check_signal():
    df = yf.download(PAIR, interval=INTERVAL, period=PERIOD, progress=False)
    df['EMA9'] = ta.ema(df['Close'], length=9)
    df['EMA20'] = ta.ema(df['Close'], length=20)

    if len(df) < 2:
        return

    last = df.iloc[-1]
    prev = df.iloc[-2]

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if prev['EMA9'] < prev['EMA20'] and last['EMA9'] > last['EMA20']:
        # BUY signal
        entry = round(last['Close'], 5)
        sl = round(entry - 0.0010, 5)
        tp = round(entry + 0.0030, 5)
        msg = f"📈 BUY SIGNAL - EUR/USD\nTime: {now}\nEntry: {entry}\nSL: {sl}\nTP: {tp}"
        send_signal(msg)

    elif prev['EMA9'] > prev['EMA20'] and last['EMA9'] < last['EMA20']:
        # SELL signal
        entry = round(last['Close'], 5)
        sl = round(entry + 0.0010, 5)
        tp = round(entry - 0.0030, 5)
        msg = f"📉 SELL SIGNAL - EUR/USD\nTime: {now}\nEntry: {entry}\nSL: {sl}\nTP: {tp}"
        send_signal(msg)

if __name__ == "__main__":
    print("📡 Forex Signal Bot Started")
    while True:
        try:
            check_signal()
        except Exception as e:
            print("❌ Error:", e)
        time.sleep(SLEEP_TIME)
