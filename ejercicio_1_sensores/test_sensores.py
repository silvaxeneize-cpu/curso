from sensores import limpiar_registro_sensor, generar_resumen_sensores

def test_limpieza_basica():
    r = limpiar_registro_sensor({"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"})
    assert r == {"sensor_id": "SENSOR-001", "temperatura": 24.5, "ubicacion": "Planta Norte"}
    assert isinstance(r["temperatura"], float)

def test_temperatura_con_simbolos_y_numero():
    assert limpiar_registro_sensor({"sensor_id": "X", "temperatura": "31.2 °C", "ubicacion": "P"})["temperatura"] == 31.2
    assert limpiar_registro_sensor({"sensor_id": "X", "temperatura": 22, "ubicacion": "P"})["temperatura"] == 22.0

def test_temperatura_corrupta_da_0():
    assert limpiar_registro_sensor({"sensor_id": "X", "temperatura": "corrupta", "ubicacion": "P"})["temperatura"] == 0.0

def test_ubicacion_por_defecto():
    assert limpiar_registro_sensor({"sensor_id": "X", "temperatura": "20C"})["ubicacion"] == "Área No Asignada"
    assert limpiar_registro_sensor({"sensor_id": "X", "temperatura": "20C", "ubicacion": "  "})["ubicacion"] == "Área No Asignada"

def test_no_muta_original():
    crudo = {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"}
    limpiar_registro_sensor(crudo)
    assert crudo["sensor_id"] == " SENSOR-001 "

def test_resumen():
    limpios = [{"sensor_id": "A", "temperatura": 20.0, "ubicacion": "P1"}, {"sensor_id": "B", "temperatura": 35.0, "ubicacion": "P1"}]
    assert generar_resumen_sensores(limpios, 30.0) == (["B"], 27.5)
    assert generar_resumen_sensores([], 30.0) == ([], 0.0)
