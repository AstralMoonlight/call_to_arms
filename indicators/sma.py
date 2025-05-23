# /call_to_arms/indicators/sma.py

"""
Módulo de cálculo de medias móviles simples (SMA) para el proyecto Call to Arms.

Incluye funciones para calcular SMA de corto y largo plazo a partir del precio de cierre.
Las SMA se usan para detectar tendencias generales en el mercado.

Autor: Ioni (AstralMoonlight)
Fecha de creación: 2025-05-22
"""

import pandas as pd

def calcular_sma(df, columna='close', corto=25, largo=75):
    """
    Agrega al DataFrame las columnas de SMA de corto y largo plazo.

    Parámetros:
    - df (pd.DataFrame): DataFrame que contiene la columna de precios.
    - columna (str): Nombre de la columna sobre la que se calcularán las SMAs.
    - corto (int): Ventana de la media móvil de corto plazo.
    - largo (int): Ventana de la media móvil de largo plazo.

    Retorna:
    - pd.DataFrame: DataFrame original con columnas 'SMA25' y 'SMA75' agregadas.
    """
    df[f"SMA{corto}"] = df[columna].rolling(window=corto).mean()
    df[f"SMA{largo}"] = df[columna].rolling(window=largo).mean()
    return df
