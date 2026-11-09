"""Ejercicio 3 Punto B - Vista Django."""
import csv, json, os
from django.shortcuts import render
from emisiones import obtener_metricas_consumo

# Datos de ejemplo realistas (pueden venir de CSV / JSON / diccionario).
# Para usar un CSV: ver _cargar_desde_csv() abajo.
REGISTROS_EJEMPLO = [
    {"planta": "Planta Norte", "consumo_kwh": 1200.5},
    {"planta": "Planta Sur", "consumo_kwh": 3400.0},
    {"planta": "Planta Este", "consumo_kwh": 800.0},
    {"planta": "Planta Norte", "consumo_kwh": 950.0},
]

def _cargar_desde_csv(ruta_csv):
    registros = []
    with open(ruta_csv, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            registros.append({"planta": fila["planta"], "consumo_kwh": float(fila["consumo_kwh"])})
    return registros

def vista_panel_sustentabilidad(request):
    """Invoca obtener_metricas_consumo y entrega el contexto a la plantilla."""
    registros = REGISTROS_EJEMPLO
    # Alternativa con CSV: registros = _cargar_desde_csv("consumo.csv")
    metricas = obtener_metricas_consumo(registros)
    contexto = {
        "total_consumo_kwh": metricas["total_consumo_kwh"],
        "total_emisiones_kg_co2": metricas["total_emisiones_kg_co2"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "detalle": metricas["detalle"],
        "registros": registros,
    }
    return render(request, "sustentabilidad/panel.html", contexto)
