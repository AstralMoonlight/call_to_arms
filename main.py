# /call_to_arms/main.py

"""
Archivo principal del proyecto Call to Arms.

Este script conecta con Binance Futures Testnet, obtiene velas recientes,
convierte los datos en un DataFrame, y calcula indicadores técnicos (RSI, SMA, volumen, ADX).
Finalmente, evalúa una señal de trading.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""

import pandas as pd
from broker_api.binance import obtener_klines
from indicators.rsi import calcular_rsi
from indicators.sma import calcular_sma
from indicators.volumen import calcular_volumen_promedio
from indicators.adx import calcular_adx
from signal_engine.analizador import determinar_senal
from config.config import (
    RSI_PERIOD, 
    SMA_CORTO, SMA_LARGO, 
    SMA_CORTO_LABEL, SMA_LARGO_LABEL,
    SYMBOL, INTERVAL, VELAS_LIMIT,
    VOLUMEN_VENTANA,
    ADX_PERIODO
)

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

    print(f"[📊] Calculando {SMA_CORTO_LABEL} y {SMA_LARGO_LABEL}...")
    df = calcular_sma(df, corto=SMA_CORTO, largo=SMA_LARGO)

    print("[📡] Calculando ADX...")
    df = calcular_adx(df, periodo=ADX_PERIODO)

    print("[📦] Calculando volumen promedio...")
    df = calcular_volumen_promedio(df, ventana=VOLUMEN_VENTANA)

    print("\n📋 Últimas 10 velas con indicadores:")
    print(df[["timestamp", "close", "RSI", SMA_CORTO_LABEL, SMA_LARGO_LABEL, "volume", "vol_prom", "ADX"]].tail(10))

    print("\n[📢] Evaluando señal...")
    señal = determinar_senal(df)
    print(f"[🔔] Señal actual para {SYMBOL}: {señal}")

if __name__ == "__main__":
    main()
