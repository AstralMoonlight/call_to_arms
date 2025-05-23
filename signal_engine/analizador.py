# /call_to_arms/signal_engine/analizador.py

"""
Analizador de señales para el bot Call to Arms.

Evalúa las condiciones técnicas en base a los indicadores calculados (RSI, SMA).
Detecta señales básicas de compra y venta.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""
from config.config import SMA_CORTO_LABEL, SMA_LARGO_LABEL
def determinar_senal(df):
    """
    Determina la señal basada en la última fila del DataFrame.

    Condiciones:
    - Señal de COMPRA si:
        RSI < 30 y SMA25 cruza por encima de SMA75
    - Señal de VENTA si:
        RSI > 70 y SMA25 cruza por debajo de SMA75
    - En otro caso:
        Mantener

    Parámetros:
    - df (pd.DataFrame): DataFrame con columnas 'RSI', 'SMA25', 'SMA75'

    Retorna:
    - str: '🟢 Compra', '🔴 Venta' o '⚪ Mantener'
    """
    if len(df) < 2:
        return "⚪ Insuficiente"

    actual = df.iloc[-1]
    anterior = df.iloc[-2]

    rsi = actual["RSI"]
    sma_c = actual[SMA_CORTO_LABEL]
    sma_l = actual[SMA_LARGO_LABEL]
    sma_c_prev = anterior[SMA_CORTO_LABEL]
    sma_l_prev = anterior[SMA_LARGO_LABEL]

    if rsi < 30 and sma_c > sma_l and sma_c_prev <= sma_l_prev:
        return "🟢 Compra"
    elif rsi > 70 and sma_c < sma_l and sma_c_prev >= sma_l_prev:
        return "🔴 Venta"
    else:
        return "⚪ Mantener"
