"""Ejercicio 3 - Auditoría de emisiones + métricas (40 pts)."""

def calcular_emisiones_carbono(consumo_kwh: float, factor_emision: float = 0.4) -> float:
    """Emisiones (kg CO2) = consumo_kwh * factor_emision. Eleva ValueError si consumo < 0."""
    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo")
    return round(float(consumo_kwh) * float(factor_emision), 2)

def obtener_metricas_consumo(registros):
    """registros: lista de dicts {"planta": str, "consumo_kwh": float} o {"planta", "consumo"}.

    Retorna dict con total_consumo_kwh, total_emisiones_kg_co2,
    planta_mayor_consumo y detalle por planta.
    """
    if not registros:
        return {"total_consumo_kwh": 0.0, "total_emisiones_kg_co2": 0.0,
                "planta_mayor_consumo": None, "detalle": []}
    por_planta = {}
    for r in registros:
        planta = r.get("planta", "Sin nombre")
        consumo = float(r.get("consumo_kwh", r.get("consumo", 0)))
        por_planta[planta] = por_planta.get(planta, 0.0) + consumo
    total_consumo = round(sum(por_planta.values()), 2)
    total_emisiones = calcular_emisiones_carbono(total_consumo)
    mayor = max(por_planta, key=por_planta.get)
    detalle = [{"planta": p, "consumo_kwh": round(c, 2),
                "emisiones_kg_co2": calcular_emisiones_carbono(c)} for p, c in por_planta.items()]
    return {"total_consumo_kwh": total_consumo, "total_emisiones_kg_co2": total_emisiones,
            "planta_mayor_consumo": mayor, "detalle": detalle}
