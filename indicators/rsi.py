# /call_to_arms/indicators/rsi.py

"""
Módulo RSI para el proyecto Call to Arms.

Este módulo contiene la función `calcular_rsi`, que calcula el índice de fuerza relativa (RSI)
a partir de una serie de precios. El RSI es un oscilador que mide la velocidad y el cambio 
de los movimientos del precio, y se utiliza comúnmente para detectar condiciones de 
sobrecompra o sobreventa.

Autor: Ioni (AstralMoonlight)
Fecha de creación: 2025-05-22
"""

import pandas as pd

def calcular_rsi(df, periodo=14, columna='close'):
    """
    Calcula el RSI (Relative Strength Index) para un DataFrame de precios.

    Parámetros:
    - df (pd.DataFrame): DataFrame que contiene al menos una columna de precios.
    - periodo (int): Número de periodos para calcular el RSI (default: 14).
    - columna (str): Nombre de la columna sobre la que se calcula el RSI (default: 'close').

    Retorna:
    - pd.Series: Serie de valores RSI con el mismo índice que `df`.
    """
    delta = df[columna].diff()
    ganancia = delta.clip(lower=0)
    perdida = -delta.clip(upper=0)

    media_ganancia = ganancia.rolling(window=periodo).mean()
    media_perdida = perdida.rolling(window=periodo).mean()

    rs = media_ganancia / media_perdida
    rsi = 100 - (100 / (1 + rs))
    return rsi
