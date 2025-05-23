# /call_to_arms/signal_engine/analizador.py

"""
Analizador de señales para el bot Call to Arms.

Evalúa condiciones técnicas usando RSI, SMA y volumen promedio,
para determinar posibles señales de compra, venta o mantener.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""

from config.config import (
    SMA_CORTO_LABEL,
    SMA_LARGO_LABEL,
    RSI_COMPRA,
    RSI_VENTA,
)

def determinar_senal(df):
    """
    Determina la señal basada en la última fila del DataFrame.

    Condiciones:
    - Señal de COMPRA si:
        RSI < RSI_COMPRA
        SMA_corto cruza sobre SMA_largo
        Volumen actual > volumen promedio

    - Señal de VENTA si:
        RSI > RSI_VENTA
        SMA_corto cruza bajo SMA_largo
        Volumen actual > volumen promedio

    - Señal de MANTENER o SIN VOLUMEN en otros casos.

    Parámetros:
    - df (pd.DataFrame): debe contener columnas RSI, SMA_corto, SMA_largo, volume y vol_prom.

    Retorna:
    - str: señal correspondiente
    """
    if len(df) < 2:
        return "⚪ Insuficiente"

    required_cols = {"RSI", SMA_CORTO_LABEL, SMA_LARGO_LABEL, "volume", "vol_prom"}
    if not required_cols.issubset(df.columns):
        return "⚪ Faltan columnas necesarias"

    actual = df.iloc[-1]
    anterior = df.iloc[-2]

    rsi = actual["RSI"]
    sma_c = actual[SMA_CORTO_LABEL]
    sma_l = actual[SMA_LARGO_LABEL]
    sma_c_prev = anterior[SMA_CORTO_LABEL]
    sma_l_prev = anterior[SMA_LARGO_LABEL]

    volumen = actual["volume"]
    volumen_prom = actual["vol_prom"]

    if volumen < volumen_prom:
        return "⚪ Sin volumen suficiente"

    if rsi < RSI_COMPRA and sma_c > sma_l and sma_c_prev <= sma_l_prev:
        return "🟢 Compra"
    elif rsi > RSI_VENTA and sma_c < sma_l and sma_c_prev >= sma_l_prev:
        return "🔴 Venta"
    else:
        return "⚪ Mantener"
