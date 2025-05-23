# /call_to_arms/signal_engine/analizador.py

"""
Analizador de señales para el bot Call to Arms.

Evalúa condiciones técnicas usando RSI, SMA y volumen promedio,
para determinar posibles señales de compra, venta o mantener.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""

import pandas as pd
from config.config import (
    SMA_CORTO_LABEL,
    SMA_LARGO_LABEL,
    RSI_COMPRA,
    RSI_VENTA,
    ADX_MINIMO
)

def determinar_señales(df, debug=False):
    if len(df) < 2:
        return False, False

    required = {"RSI", SMA_CORTO_LABEL, SMA_LARGO_LABEL, "volume", "vol_prom", "ADX"}
    if not required.issubset(df.columns):
        return False, False

    actual = df.iloc[-1]
    anterior = df.iloc[-2]

    rsi = actual["RSI"]
    sma_c = actual[SMA_CORTO_LABEL]
    sma_l = actual[SMA_LARGO_LABEL]
    sma_c_prev = anterior[SMA_CORTO_LABEL]
    sma_l_prev = anterior[SMA_LARGO_LABEL]
    volumen = actual["volume"]
    volumen_prom = actual["vol_prom"]
    adx = actual["ADX"]

    vol_ok = volumen > volumen_prom
    adx_ok = pd.notna(adx) and adx >= ADX_MINIMO

    long_cond = rsi < RSI_COMPRA and sma_c > sma_l and sma_c_prev <= sma_l_prev
    short_cond = rsi > RSI_VENTA and sma_c < sma_l and sma_c_prev >= sma_l_prev

    if debug:
        print("\n🔍 Evaluación de condiciones:")
        print(f"RSI = {rsi:.2f} → Long < {RSI_COMPRA}, Short > {RSI_VENTA}")
        print(f"SMA cruce: {sma_c_prev:.2f} → {sma_c:.2f} vs {sma_l_prev:.2f} → {sma_l:.2f}")
        print(f"Volumen actual: {volumen:.2f}, promedio: {volumen_prom:.2f} → {'✅' if vol_ok else '❌'}")
        print(f"ADX = {adx:.2f} (mínimo requerido: {ADX_MINIMO}) → {'✅' if adx_ok else '❌'}")
        print(f"Long válido: {'✅' if (long_cond and vol_ok and adx_ok) else '❌'}")
        print(f"Short válido: {'✅' if (short_cond and vol_ok and adx_ok) else '❌'}")

    return (long_cond and vol_ok and adx_ok), (short_cond and vol_ok and adx_ok)