# /call_to_arms/indicators/volumen.py

"""
Indicador de volumen para el bot Call to Arms.

Calcula el volumen promedio de las últimas N velas para confirmar
si hay interés real en los movimientos del mercado.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""

import pandas as pd

def calcular_volumen_promedio(df, ventana=20):
    """
    Agrega columna 'vol_prom' al DataFrame con el volumen promedio.

    Parámetros:
    - df (pd.DataFrame): DataFrame que contiene columna 'volume'.
    - ventana (int): Cantidad de velas a considerar.

    Retorna:
    - pd.DataFrame con columna nueva 'vol_prom'
    """
    df["vol_prom"] = df["volume"].rolling(window=ventana).mean()
    return df
