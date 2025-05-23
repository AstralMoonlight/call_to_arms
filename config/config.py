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


ADX_PERIODO = 14
ADX_MINIMO = 20  # Mínimo requerido para considerar que hay tendencia

VOLUMEN_VENTANA = 20  # Últimas 20 velas

# Otros ajustes globales (futuros)
SYMBOL = "BTCUSDT"
INTERVAL = "1m"
VELAS_LIMIT = 1000


# Capital y gestión de riesgo
CAPITAL_INICIAL = 100000  # CLP o USDT según contexto
PORCENTAJE_OPERAR = 5       # Porcentaje del capital usado por operación
APALANCAMIENTO = 3          # x3 por defecto
MAX_POSICIONES_SIMULTANEAS = 5  # o el número que quieras permitir

# Condiciones de salida (valores funcionales)
STOP_LOSS_PORC = 2          # SL si cae 2% desde el precio de entrada
TAKE_PROFIT_PORC = 4        # TP si sube 4% desde el precio de entrada
