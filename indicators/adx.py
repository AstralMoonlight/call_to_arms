# /call_to_arms/indicators/adx.py

"""
Indicador ADX para el proyecto Call to Arms.

Calcula la fuerza de la tendencia mediante el índice de movimiento direccional promedio (ADX),
basado en los valores de alto, bajo y cierre.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""

import pandas as pd
import numpy as np

def calcular_adx(df, periodo=14):
    """
    Calcula el ADX para un DataFrame con columnas: 'high', 'low', 'close'.

    Parámetros:
    - df (pd.DataFrame): DataFrame con columnas 'high', 'low', 'close'.
    - periodo (int): número de periodos para suavizar los cálculos (default: 14)

    Retorna:
    - pd.DataFrame con columnas nuevas: 'ADX', '+DI', '-DI'
    """
    df = df.copy()

    df['+DM'] = df['high'].diff()
    df['-DM'] = df['low'].diff()

    df['+DM'] = np.where((df['+DM'] > df['-DM']) & (df['+DM'] > 0), df['+DM'], 0)
    df['-DM'] = np.where((df['-DM'] > df['+DM']) & (df['-DM'] > 0), df['-DM'], 0)

    df['TR'] = df[['high', 'low', 'close']].copy().apply(
        lambda row: max(
            row['high'] - row['low'],
            abs(row['high'] - row['close']),
            abs(row['low'] - row['close'])
        ), axis=1
    )

    df['TR_smooth'] = df['TR'].rolling(window=periodo).mean()
    df['+DI'] = 100 * (df['+DM'].rolling(window=periodo).mean() / df['TR_smooth'])
    df['-DI'] = 100 * (df['-DM'].rolling(window=periodo).mean() / df['TR_smooth'])

    df['DX'] = 100 * (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI']))
    df['ADX'] = df['DX'].rolling(window=periodo).mean()

    return df
