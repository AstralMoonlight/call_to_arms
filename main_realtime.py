# /call_to_arms/main_realtime.py

"""
Ejecución en tiempo real del bot Call to Arms.

Cada 1 minuto se obtiene una vela nueva desde Binance Testnet,
se agrega al análisis y se evalúa si ha cambiado la señal.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""

import pandas as pd
import time
from datetime import datetime

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

def cargar_datos_iniciales():
    print("[⏳] Cargando datos históricos iniciales...")
    raw = obtener_klines(symbol=SYMBOL, interval=INTERVAL, limit=VELAS_LIMIT)
    return parsear_klines_a_df(raw)

def obtener_ultima_vela():
    raw = obtener_klines(symbol=SYMBOL, interval=INTERVAL, limit=1)
    return parsear_klines_a_df(raw)

def aplicar_indicadores(df):
    df["RSI"] = calcular_rsi(df, periodo=RSI_PERIOD)
    df = calcular_sma(df, corto=SMA_CORTO, largo=SMA_LARGO)
    df = calcular_volumen_promedio(df, ventana=VOLUMEN_VENTANA)
    df = calcular_adx(df, periodo=ADX_PERIODO)
    return df

def main():
    df = cargar_datos_iniciales()
    df = aplicar_indicadores(df)
    señal_anterior = determinar_senal(df)

    print(f"[📢] Señal base: {señal_anterior}")

    while True:
        print(f"\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Esperando nueva vela...")

        try:
            nueva = obtener_ultima_vela()
            if not nueva.empty:
                # Evitar duplicados
                if nueva["timestamp"].iloc[0] != df["timestamp"].iloc[-1]:
                    df = pd.concat([df, nueva], ignore_index=True)

                    # Mantener tamaño fijo si se desea
                    if len(df) > VELAS_LIMIT:
                        df = df.iloc[-VELAS_LIMIT:].reset_index(drop=True)

                    df = aplicar_indicadores(df)
                    señal_actual = determinar_senal(df)

                    if señal_actual != señal_anterior:
                        print(f"[⚠️] ¡Cambio de señal! {señal_anterior} → {señal_actual}")
                        señal_anterior = señal_actual
                    else:
                        print(f"[=] Sin cambio de señal ({señal_actual})")
                else:
                    print("[⏸️] Vela aún no finalizada")
        except Exception as e:
            print(f"[❌ ERROR] Falló el análisis: {e}")

        time.sleep(60)

if __name__ == "__main__":
    main()
