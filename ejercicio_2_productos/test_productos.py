import pytest, json
from productos import DispositivoEcologico, PanelSolar, StockInvalidoError, GestorInventario

def test_hereda_de_exception():
    assert issubclass(StockInvalidoError, Exception)
    assert str(StockInvalidoError()) == "El stock no puede ser un valor negativo."

def test_stock_negativo_en_constructor():
    with pytest.raises(StockInvalidoError):
        DispositivoEcologico("X-1", "X", 100, -1)

def test_stock_negativo_en_setter_con_nombre_y_valor():
    p = PanelSolar("PAN-001", "Panel Test", 100, 5, 0.22, 450)
    with pytest.raises(StockInvalidoError) as exc:
        p.stock = -5
    assert "Panel Test" in str(exc.value) and "-5" in str(exc.value)

def test_ficha_base_es_diccionario_y_precio_formateado():
    d = DispositivoEcologico("TER-001", "Termo", 320000.0, 8).generar_ficha_tecnica()
    assert isinstance(d, dict) and d["precio"] == "$320000.00" and d["stock"] == 8

def test_polimorfismo_panel():
    d = PanelSolar("PAN-001", "Panel", 100, 5, 0.22, 450).generar_ficha_tecnica()
    assert d["tipo"] == "Panel Solar" and d["potencia_w"] == 450 and d["eficiencia"] == 0.22

def test_guardar_json(tmp_path):
    ruta = tmp_path / "catalogo_ecotech.json"
    GestorInventario.guardar_catalogo_json([PanelSolar("PAN-001", "P", 100, 2, 0.22, 450)], str(ruta))
    assert json.loads(ruta.read_text(encoding="utf-8"))[0]["tipo"] == "PanelSolar"
