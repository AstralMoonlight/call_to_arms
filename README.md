# 🛡️ Call to Arms

Bot de trading automático para criptomonedas utilizando múltiples indicadores técnicos, incluyendo RSI, SMA, ADX, volumen y patrones de velas japonesas.

## Características
- Operaciones long y short vía Binance Futures Testnet
- Módulo de señales técnicas con análisis combinados
- Gestión de riesgo integrada
- Conectividad vía API
- Registro de operaciones

## Estructura
- `indicators/`: Cálculo de indicadores individuales
- `strategies/`: Lógica de trading combinada
- `broker_api/`: Interfaz con el exchange
- `signal_engine/`: Generador de señales
- `risk_management/`: Tamaño de posición, SL, TP
- `logs/`: Registro de resultados
- `config/`: Parámetros y configuración del bot

---

## Próximo paso

¿Querés que empecemos con el archivo de conexión a Binance Testnet (`broker_api/binance.py`) o prefieres comenzar con los indicadores (`indicators/rsi.py`, etc.)?
