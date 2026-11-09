"""Ver el panel en el navegador - sin crear un proyecto Django completo.
Uso:
    pip install Django
    python ver_panel.py
Luego abrir: http://127.0.0.1:8000/panel/
Ctrl+C para detener el servidor.
"""
import os, sys
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from django.conf import settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="ecotech-demo",
        ALLOWED_HOSTS=["*"],
        ROOT_URLCONF="ver_panel",
        TEMPLATES=[{
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE, "sustentabilidad", "templates")],
            "APP_DIRS": False,
        }],
    )
    import django
    django.setup()

from django.urls import path
from django.shortcuts import render, redirect
from emisiones import obtener_metricas_consumo

REGISTROS_EJEMPLO = [
    {"planta": "Planta Norte", "consumo_kwh": 1200.5},
    {"planta": "Planta Sur", "consumo_kwh": 3400.0},
    {"planta": "Planta Este", "consumo_kwh": 800.0},
    {"planta": "Planta Norte", "consumo_kwh": 950.0},
]

def vista_panel_sustentabilidad(request):
    """La misma vista del Ejercicio 3 Punto B."""
    metricas = obtener_metricas_consumo(REGISTROS_EJEMPLO)
    contexto = {
        "total_consumo_kwh": metricas["total_consumo_kwh"],
        "total_emisiones_kg_co2": metricas["total_emisiones_kg_co2"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "detalle": metricas["detalle"],
        "registros": REGISTROS_EJEMPLO,
    }
    return render(request, "sustentabilidad/panel.html", contexto)

def inicio(request):
    return redirect("/panel/")

urlpatterns = [
    path("", inicio),
    path("panel/", vista_panel_sustentabilidad, name="panel_sustentabilidad"),
]

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], "runserver", "8000"])
