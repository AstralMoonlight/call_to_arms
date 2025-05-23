# /call_to_arms/main.py

"""
Archivo principal del proyecto Call to Arms.

Este script conecta con Binance Futures Testnet, obtiene velas recientes,
convierte los datos en un DataFrame de pandas, y calcula el RSI (Relative Strength Index).
Se utiliza como punto de entrada para análisis y pruebas de señales técnicas.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""

import pandas as pd
from broker_api.binance import obtener_klines
from indicators.rsi import calcular_rsi

def parsear_klines_a_df(raw_klines):
    """
    Convierte una lista de klines en un DataFrame con columnas estándar.

    Parámetros:
    - raw_klines (list): Lista cruda de velas devuelta por Binance.

    Retorna:
    - pd.DataFrame: DataFrame con columnas ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    """
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
    raw_klines = obtener_klines(symbol="BTCUSDT", interval="1m", limit=100)
    df = parsear_klines_a_df(raw_klines)

    print("[📈] Calculando RSI...")
    df["RSI"] = calcular_rsi(df)

    print(df[["timestamp", "close", "RSI"]].tail(10))  # Mostrar las últimas 10 filas

if __name__ == "__main__":
    main()
