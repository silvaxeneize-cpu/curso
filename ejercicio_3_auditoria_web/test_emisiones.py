"""Ejercicio 3 Punto A - Auditoría con unittest."""
import unittest
from emisiones import calcular_emisiones_carbono, obtener_metricas_consumo

class TestCalculoEmisiones(unittest.TestCase):
    def test_valor_nominal_factor_por_defecto(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)

    def test_valor_nominal_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100, factor_emision=0.5), 50.0)

    def test_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0.0)

    def test_decimales(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(12.5), 5.0)

    def test_consumo_negativo_eleva_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-1)
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-100.5)

class TestMetricasConsumo(unittest.TestCase):
    def test_total_y_mayor_consumo(self):
        m = obtener_metricas_consumo([
            {"planta": "Planta Norte", "consumo_kwh": 1000},
            {"planta": "Planta Sur", "consumo_kwh": 2500},
            {"planta": "Planta Norte", "consumo_kwh": 500},
        ])
        self.assertEqual(m["total_consumo_kwh"], 4000)
        self.assertEqual(m["total_emisiones_kg_co2"], 1600.0)
        self.assertEqual(m["planta_mayor_consumo"], "Planta Sur")

    def test_vacio(self):
        m = obtener_metricas_consumo([])
        self.assertEqual(m["total_emisiones_kg_co2"], 0.0)
        self.assertIsNone(m["planta_mayor_consumo"])

if __name__ == "__main__":
    unittest.main()
