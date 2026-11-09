"""Ejercicio 1 - Sanitización y Análisis Estadístico de Sensores.
Paso 1.1: limpiar_registro_sensor
Paso 1.2: generar_resumen_sensores
"""

# Paso 1.1: Diseñar la Función de Normalización
def limpiar_registro_sensor(registro_raw: dict) -> dict:
    """Recibe un diccionario crudo y retorna un nuevo diccionario estandarizado."""
    # 1. Definición e Inicialización: diccionario vacío, no se muta el original
    registro_limpio = {}

    # 2. Sanitización del Identificador (sensor_id)
    sensor_id = registro_raw.get("sensor_id", "")
    if sensor_id is None:
        sensor_id = ""
    sensor_id = str(sensor_id).strip()
    registro_limpio["sensor_id"] = sensor_id

    # 3. Estandarización de la Temperatura (temperatura)
    temperatura_raw = registro_raw.get("temperatura", 0)
    if isinstance(temperatura_raw, (int, float)) and not isinstance(temperatura_raw, bool):
        temperatura = float(temperatura_raw)
    else:
        texto = str(temperatura_raw)
        texto = texto.replace("C", "").replace("c", "").replace("F", "").replace("f", "")
        texto = texto.replace("°", "").replace(" ", "").replace(",", ".")
        try:
            temperatura = float(texto)
        except ValueError:
            temperatura = 0.0
    registro_limpio["temperatura"] = temperatura

    # 4. Tratamiento del Atributo de Ubicación (ubicacion)
    ubicacion = registro_raw.get("ubicacion")
    if ubicacion is None or str(ubicacion).strip() == "":
        registro_limpio["ubicacion"] = "Área No Asignada"
    else:
        registro_limpio["ubicacion"] = str(ubicacion).strip()

    # 5. Retorno de Datos
    return registro_limpio


# Paso 1.2: Diseñar la Función de Mapeo Estadístico
def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura: float):
    """Retorna una tupla (lista_sensores_alerta, promedio_temperatura)."""
    if not lista_sensores_limpios:
        return ([], 0.0)
    acumulador = 0.0
    lista_alertas = []
    for sensor in lista_sensores_limpios:
        temperatura = sensor["temperatura"]
        acumulador += temperatura
        if temperatura > umbral_temperatura:
            lista_alertas.append(sensor["sensor_id"])
    promedio = round(acumulador / len(lista_sensores_limpios), 2)
    return (lista_alertas, promedio)


if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": "31.2 °C", "ubicacion": "Planta Sur"},
        {"sensor_id": " SENSOR-003 ", "temperatura": "28.0C", "ubicacion": ""},
        {"sensor_id": "SENSOR-004", "temperatura": " 35.0 C ", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-005", "temperatura": 22.1, "ubicacion": "  Planta Este  "},
        {"sensor_id": "SENSOR-006", "temperatura": "corrupta", "ubicacion": "Planta Sur"},
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
