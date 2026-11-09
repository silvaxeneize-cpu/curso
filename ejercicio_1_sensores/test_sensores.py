import pytest
from sensores import limpiar_registro_sensor, generar_resumen_sensores

def test_limpieza_basica():
    r = limpiar_registro_sensor({"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"})
    assert r == {"sensor_id": "SENSOR-001", "temperatura": 24.5, "ubicacion": "Planta Norte"}
    assert isinstance(r["temperatura"], float)

def test_ubicacion_por_defecto():
    assert limpiar_registro_sensor({"sensor_id": "X", "temperatura": "20C"})["ubicacion"] == "Sin ubicación"
    assert limpiar_registro_sensor({"sensor_id": "X", "temperatura": "20C", "ubicacion": "  "})["ubicacion"] == "Sin ubicación"

def test_resumen():
    limpios = [{"sensor_id": "A", "temperatura": 20.0, "ubicacion": "P1"}, {"sensor_id": "B", "temperatura": 35.0, "ubicacion": "P1"}]
    alerta, prom = generar_resumen_sensores(limpios, 30.0)
    assert alerta == ["B"] and prom == 27.5
    assert generar_resumen_sensores([], 30.0) == ([], 0.0)
