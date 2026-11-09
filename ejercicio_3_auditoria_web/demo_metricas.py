from emisiones import obtener_metricas_consumo
if __name__ == "__main__":
    registros = [
        {"planta": "Planta Norte", "consumo_kwh": 1200.5},
        {"planta": "Planta Sur", "consumo_kwh": 3400.0},
        {"planta": "Planta Este", "consumo_kwh": 800.0},
    ]
    print(obtener_metricas_consumo(registros))
