# /call_to_arms/broker_api/binance.py

import requests
import time

# Base URL para Binance Futures Testnet
BASE_URL = "https://testnet.binancefuture.com"

def obtener_klines(symbol="BTCUSDT", interval="1m", limit=10):
    url = f"{BASE_URL}/fapi/v1/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        datos = response.json()
        return datos
    except Exception as e:
        print(f"[❌] Error al obtener klines: {e}")
        return []

# Para probar directamente
if __name__ == "__main__":
    klines = obtener_klines()
    for vela in klines:
        print(vela)
