import os
import requests
from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
from market_data import get_xauusd_data

load_dotenv()

app = FastAPI()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

def send_telegram_message(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/test-data")
def test_data():
    return get_xauusd_data()  

@app.post("/webhook/tradingview")
async def tradingview_webhook(request: Request):
    data = await request.json()

    if data.get("secret") != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")

    symbol = data.get("symbol", "UNKNOWN")
    timeframe = data.get("timeframe", "UNKNOWN")
    direction = data.get("direction", "UNKNOWN")
    rr = data.get("rr", "N/A")
    entry_zone = data.get("entry_zone", "N/A")
    stop_loss = data.get("stop_loss", "N/A")
    take_profit = data.get("take_profit", "N/A")
    confidence = data.get("confidence", "N/A")

    message = (
        f"{symbol} {timeframe} — {direction.upper()} signal\n\n"
        f"Entry: {entry_zone}\n"
        f"SL: {stop_loss}\n"
        f"TP: {take_profit}\n"
        f"R:R: {rr}\n"
        f"Confidence: {confidence}"
    )

    send_telegram_message(message)
    return {"ok": True}