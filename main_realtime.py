# /call_to_arms/main_realtime.py

"""
Ejecución en tiempo real del bot Call to Arms.

Cada 1 minuto se obtiene una vela nueva desde Binance Testnet,
se agrega al análisis, se recalculan indicadores, se evalúan señales
para longs y shorts, y se simulan operaciones afectando el capital.
También se guarda un log con cada operación realizada.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""

import pandas as pd
import time
from datetime import datetime
import os

from broker_api.binance import obtener_klines
from indicators.rsi import calcular_rsi
from indicators.sma import calcular_sma
from indicators.volumen import calcular_volumen_promedio
from indicators.adx import calcular_adx
from signal_engine.analizador import determinar_señales
from risk_management.cartera import Cartera

from config.config import (
    RSI_PERIOD,
    SMA_CORTO, SMA_LARGO,
    SMA_CORTO_LABEL, SMA_LARGO_LABEL,
    SYMBOL, INTERVAL, VELAS_LIMIT,
    VOLUMEN_VENTANA,
    ADX_PERIODO
)

LOG_PATH = "logs/historial_operaciones.log"

def parsear_klines_a_df(raw_klines):
    try:
        datos = [
            {
                'timestamp': int(k[0]),
                'open': float(k[1]),
                'high': float(k[2]),
                'low': float(k[3]),
                'close': float(k[4]),
                'volume': float(k[5]),
            } for k in raw_klines
        ]
        df = pd.DataFrame(datos)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"[❌] Error al parsear datos de Binance: {e}")
        return pd.DataFrame()

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

def registrar_en_log(texto):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {texto}\n")

def main():
    df = cargar_datos_iniciales()
    df = aplicar_indicadores(df)
    cartera = Cartera()

    print(f"[💼] Capital inicial: {cartera.capital:.2f}")

    while True:
        print(f"\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Esperando nueva vela...")

        try:
            nueva = obtener_ultima_vela()
            if not nueva.empty:
                if nueva["timestamp"].iloc[0] != df["timestamp"].iloc[-1]:
                    df = pd.concat([df, nueva], ignore_index=True)
                    if len(df) > VELAS_LIMIT:
                        df = df.iloc[-VELAS_LIMIT:].reset_index(drop=True)

                    df = aplicar_indicadores(df)
                    precio_actual = df["close"].iloc[-1]

                    resultados = cartera.evaluar_operaciones(precio_actual)
                    for pos, motivo in resultados:
                        cierre = cartera.cerrar_operacion(pos, precio_actual, motivo)
                        print(cierre)
                        registrar_en_log(cierre)

                    long_valido, short_valido = determinar_señales(df, debug=True)

                    if long_valido:
                        apertura = cartera.abrir_operacion(precio_actual, tipo="long")
                        print(apertura)
                        registrar_en_log(apertura)
                    if short_valido:
                        apertura = cartera.abrir_operacion(precio_actual, tipo="short")
                        print(apertura)
                        registrar_en_log(apertura)
                else:
                    print("[⏸️] Vela aún no finalizada")
        except Exception as e:
            print(f"[❌ ERROR] Falló el análisis: {e}")

        time.sleep(60)

if __name__ == "__main__":
    main()
