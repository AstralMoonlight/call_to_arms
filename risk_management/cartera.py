# /call_to_arms/risk_management/cartera.py

"""
Módulo extendido de gestión de capital para múltiples posiciones simultáneas.

Autor: Ioni (AstralMoonlight)
Fecha: 2025-05-23
"""

from config.config import (
    CAPITAL_INICIAL, PORCENTAJE_OPERAR, APALANCAMIENTO,
    STOP_LOSS_PORC, TAKE_PROFIT_PORC, MAX_POSICIONES_SIMULTANEAS
)

import uuid

class Cartera:
    def __init__(self):
        self.capital = CAPITAL_INICIAL
        self.posiciones = []  # [{id, tipo, entrada}]
        self.transacciones = []

    def calcular_tamaño_operacion(self):
        return (self.capital * (PORCENTAJE_OPERAR / 100)) * APALANCAMIENTO

    def abrir_operacion(self, precio, tipo="long"):
        if len(self.posiciones) >= MAX_POSICIONES_SIMULTANEAS:
            return "[❌] Máximo de posiciones simultáneas alcanzado."

        monto = self.calcular_tamaño_operacion()
        posicion = {
            "id": str(uuid.uuid4())[:8],
            "tipo": tipo,
            "entrada": precio,
            "monto": monto
        }
        self.posiciones.append(posicion)
        return f"[📈] {tipo.upper()} abierta a {precio:.2f} (id: {posicion['id']})"

    def evaluar_operaciones(self, precio_actual):
        cerradas = []
        for pos in self.posiciones:
            cambio_pct = ((precio_actual - pos["entrada"]) / pos["entrada"]) * 100
            if pos["tipo"] == "short":
                cambio_pct *= -1

            if cambio_pct <= -STOP_LOSS_PORC:
                cerradas.append((pos, "SL"))
            elif cambio_pct >= TAKE_PROFIT_PORC:
                cerradas.append((pos, "TP"))

        return cerradas

    def cerrar_operacion(self, posicion, precio_actual, motivo):
        cambio_pct = ((precio_actual - posicion["entrada"]) / posicion["entrada"]) * 100
        if posicion["tipo"] == "short":
            cambio_pct *= -1

        ganancia = posicion["monto"] * (cambio_pct / 100)
        self.capital += ganancia
        self.posiciones.remove(posicion)

        resumen = f"[💰] Cierre {motivo}: {posicion['tipo']} #{posicion['id']} a {precio_actual:.2f} | Δ={cambio_pct:.2f}% | {'+' if ganancia >= 0 else ''}{ganancia:.2f} | Capital: {self.capital:.2f}"
        self.transacciones.append({
            "id": posicion["id"],
            "tipo": posicion["tipo"],
            "entrada": posicion["entrada"],
            "salida": precio_actual,
            "motivo": motivo,
            "ganancia": ganancia,
            "capital_final": self.capital
        })
        return resumen
