# ECOTECH SOLUTIONS – Evaluación Técnica de Desarrollo

## Estructura
- `ejercicio_1_sensores/` — Sanitización y análisis estadístico de sensores
- `ejercicio_2_productos/` — Modelo de productos, excepciones y persistencia
- `ejercicio_3_auditoria_web/` — Auditoría con tests unitarios e integración web (Django)

## Cómo ejecutar
```bash
# Ejercicio 1
python ejercicio_1_sensores/sensores.py

# Ejercicio 2
python ejercicio_2_productos/productos.py

# Ejercicio 3 - tests
python -m pytest ejercicio_3_auditoria_web/test_emisiones.py -v
# o con unittest:
python -m unittest ejercicio_3_auditoria_web.test_emisiones -v
python ejercicio_3_auditoria_web/demo_metricas.py
```

## Requisitos
Python 3.9+ . pytest opcional. Django solo necesario para servir la vista (ver ejercicio_3).
