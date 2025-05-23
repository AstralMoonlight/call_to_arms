# /call_to_arms/config/config.py

"""
Archivo de configuración para el proyecto Call to Arms.

Contiene los parámetros ajustables para los indicadores técnicos usados en el bot:
RSI, SMA y otros.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-22
"""

# Parámetros para RSI
RSI_PERIOD = 14
RSI_COMPRA = 30   # valor bajo: sobreventa
RSI_VENTA  = 70   # valor alto: sobrecompra

# Parámetros para SMA
SMA_CORTO = 25
SMA_LARGO = 75
SMA_CORTO_LABEL = f"SMA{SMA_CORTO}"
SMA_LARGO_LABEL = f"SMA{SMA_LARGO}"

# Otros ajustes globales (futuros)
SYMBOL = "BTCUSDT"
INTERVAL = "1m"
VELAS_LIMIT = 100
VOLUMEN_VENTANA = 20  # Últimas 20 velas