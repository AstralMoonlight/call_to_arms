# /call_to_arms/main.py

"""
Archivo principal del proyecto Call to Arms.

Este script conecta con Binance Futures Testnet, obtiene velas recientes,
convierte los datos en un DataFrame, y calcula indicadores técnicos (RSI y SMA).
Es el punto de entrada para el análisis.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""

import pandas as pd
from broker_api.binance import obtener_klines
from indicators.rsi import calcular_rsi
from indicators.sma import calcular_sma
from config.config import RSI_PERIOD, SMA_CORTO, SMA_LARGO, SYMBOL, INTERVAL, VELAS_LIMIT

def parsear_klines_a_df(raw_klines):
    columnas = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    datos = [
        {
            'timestamp': int(k[0]),
            'open': float(k[1]),
            'high': float(k[2]),
            'low': float(k[3]),
            'close': float(k[4]),
            'volume': float(k[5]),
        }
        for k in raw_klines
    ]
    df = pd.DataFrame(datos)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def main():
    print("[⚙️] Obteniendo datos desde Binance Futures Testnet...")
    raw_klines = obtener_klines(symbol=SYMBOL, interval=INTERVAL, limit=VELAS_LIMIT)
    df = parsear_klines_a_df(raw_klines)

    print("[📈] Calculando RSI...")
    df["RSI"] = calcular_rsi(df, periodo=RSI_PERIOD)

    print("[📊] Calculando SMA25 y SMA75...")
    df = calcular_sma(df, corto=SMA_CORTO, largo=SMA_LARGO)

    print(df[["timestamp", "close", "RSI", "SMA25", "SMA75"]].tail(10))  # Últimas 10 filas

if __name__ == "__main__":
    main()
