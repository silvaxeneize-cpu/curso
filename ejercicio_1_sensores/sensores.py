"""Ejercicio 1 - Sanitización y Análisis Estadístico de Sensores (20 pts)."""
import re
from typing import Any

def limpiar_registro_sensor(registro_raw: dict) -> dict:
    """Normaliza un registro crudo de sensor.

    - sensor_id: sin espacios sobrantes (strip). Si falta/vacío -> "DESCONOCIDO".
    - temperatura: float sin sufijos de unidad ("24.5C", " 24,5 °C ", "24.5") -> 24.5
    - ubicacion: valor por defecto seguro "Sin ubicación" si falta/vacía/None.
    No muta el diccionario original: retorna uno nuevo.
    """
    if not isinstance(registro_raw, dict):
        raise TypeError("registro_raw debe ser un diccionario")

    sensor_id = registro_raw.get("sensor_id", "")
    if sensor_id is None:
        sensor_id = ""
    sensor_id = str(sensor_id).strip() or "DESCONOCIDO"

    temp_raw = registro_raw.get("temperatura", 0)
    temperatura = _parse_temperatura(temp_raw)

    ubicacion = registro_raw.get("ubicacion")
    if ubicacion is None or str(ubicacion).strip() == "":
        ubicacion = "Sin ubicación"
    else:
        ubicacion = str(ubicacion).strip()

    return {"sensor_id": sensor_id, "temperatura": temperatura, "ubicacion": ubicacion}

def _parse_temperatura(valor: Any) -> float:
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        return float(valor)
    if valor is None or (isinstance(valor, str) and valor.strip() == ""):
        return 0.0
    texto = str(valor).strip()
    # Acepta coma decimal, quita unidades / símbolos: "24,5 °C" -> "24.5"
    texto = texto.replace(",", ".")
    match = re.search(r"-?\d+(?:\.\d+)?", texto)
    if not match:
        raise ValueError(f"No se pudo interpretar la temperatura: {valor!r}")
    return float(match.group(0))

def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura: float):
    """Retorna (lista_sensores_alerta, promedio_temperatura).

    lista_sensores_alerta: IDs con temperatura > umbral.
    promedio_temperatura: promedio global, 0.0 si la lista está vacía.
    """
    if not lista_sensores_limpios:
        return ([], 0.0)
    alerta = [r["sensor_id"] for r in lista_sensores_limpios if r["temperatura"] > umbral_temperatura]
    promedio = sum(r["temperatura"] for r in lista_sensores_limpios) / len(lista_sensores_limpios)
    return (alerta, round(promedio, 2))

if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": "31.2 °C", "ubicacion": "Planta Sur"},
        {"sensor_id": " SENSOR-003 ", "temperatura": "28.0C"},
        {"sensor_id": "SENSOR-004", "temperatura": " 35.7C ", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-005", "temperatura": 22.1, "ubicacion": "  Planta Este  "},
    ]
    umbral = 30.0
    limpios = [limpiar_registro_sensor(r) for r in registros_crudos]
    alerta, promedio = generar_resumen_sensores(limpios, umbral)

    print("=== ECOTECH SOLUTIONS - Reporte de Sensores ===")
    for r in limpios:
        print(f"{r['sensor_id']:<12} | {r['temperatura']:>5.1f} °C | {r['ubicacion']}")
    print("-" * 50)
    print(f"Umbral de alerta: {umbral} °C")
    print(f"Promedio global: {promedio} °C")
    print(f"Sensores en alerta ({len(alerta)}): {', '.join(alerta) if alerta else 'Ninguno'}")
