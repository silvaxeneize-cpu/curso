import pytest, json, pathlib
from productos import DispositivoEcologico, PanelSolar, StockInvalidoError, GestorInventario

def test_stock_negativo_en_constructor():
    with pytest.raises(StockInvalidoError):
        DispositivoEcologico("X", 100, -1)

def test_stock_negativo_en_setter():
    p = PanelSolar("P", 100, 5, 450, 0.22)
    with pytest.raises(StockInvalidoError):
        p.stock = -3

def test_polimorfismo_ficha():
    p = PanelSolar("Panel 450W", 100, 5, 450, 0.22)
    assert "450W" in p.ficha_tecnica() and "22.0%" in p.ficha_tecnica()

def test_guardar_json(tmp_path):
    ruta = tmp_path / "catalogo_ecotech.json"
    GestorInventario.guardar_catalogo_json([PanelSolar("P", 100, 2, 450, 0.22)], str(ruta))
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    assert datos[0]["tipo"] == "PanelSolar" and datos[0]["stock"] == 2
