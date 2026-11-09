"""Ejercicio 2 - Modelo de Productos, Excepciones y Persistencia.
Paso 2.1: StockInvalidoError
Paso 2.2: DispositivoEcologico
Paso 2.3: PanelSolar
"""
import json

# Paso 2.1: Diseñar la Excepción Personalizada
class StockInvalidoError(Exception):
    """Hereda directamente de Exception."""
    def __init__(self, mensaje="El stock no puede ser un valor negativo."):
        super().__init__(mensaje)

# Paso 2.2: Diseñar la Clase Base del Catálogo
class DispositivoEcologico:
    def __init__(self, id_producto, nombre, precio, stock):
        # 1. Atributos públicos: asignación directa
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        # 2. Encapsulamiento: variable de respaldo privada inicializada en 0
        self._stock = 0
        # Regla de Consistencia: invocar la propiedad para forzar la validación del setter
        self.stock = stock

    @property
    def stock(self):
        """Método de lectura: retorna el valor oculto."""
        return self._stock

    @stock.setter
    def stock(self, valor):
        """Método de escritura con validación."""
        if valor < 0:
            raise StockInvalidoError(
                f"Stock inválido para '{self.nombre}': se intentó asignar {valor}. "
                "El stock no puede ser un valor negativo."
            )
        self._stock = valor

    # 4. Diseño de la Ficha Técnica Base: retorna un diccionario
    def generar_ficha_tecnica(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": f"${self.precio:.2f}",
            "stock": self.stock,
        }

    def to_dict(self):
        # Para persistencia en JSON: ficha + tipo
        d = self.generar_ficha_tecnica()
        d["tipo"] = type(self).__name__
        return d

    def __repr__(self):
        return f"{type(self).__name__}(id_producto={self.id_producto!r}, nombre={self.nombre!r}, precio={self.precio}, stock={self.stock})"

# Paso 2.3: Diseñar la Subclase Especializada
class PanelSolar(DispositivoEcologico):
    def __init__(self, id_producto, nombre, precio, stock, eficiencia, potencia_w):
        # Invocar en la primera línea el constructor de la clase superior
        super().__init__(id_producto, nombre, precio, stock)
        # Guardar localmente los atributos nuevos
        self.eficiencia = eficiencia
        self.potencia_w = potencia_w

    # Sobrescritura Polimórfica del Reporte
    def generar_ficha_tecnica(self):
        ficha_base = super().generar_ficha_tecnica()
        ficha_base.update({
            "tipo": "Panel Solar",
            "potencia_w": self.potencia_w,
            "eficiencia": self.eficiencia,
        })
        return ficha_base

class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo="catalogo_ecotech.json"):
        datos = [d.to_dict() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return ruta_archivo

if __name__ == "__main__":
    # Paso 3: Validación General - bloque de objetos
    panel = PanelSolar("PAN-001", "Panel Solar EcoTech 450W", 189999.0, 25, 0.22, 450)
    print("Ficha técnica (diccionario expandido polimórficamente):")
    print(panel.generar_ficha_tecnica())

    # Bloque try-except: intento intencional de asignar stock -5
    try:
        panel.stock = -5
    except StockInvalidoError as e:
        print(f"[ADVERTENCIA CONTROLADA] StockInvalidoError capturado: {e}")
    print(f"Stock final del panel (sin cambios): {panel.stock}")

    # Exportación de productos válidos
    catalogo = [
        panel,
        PanelSolar("PAN-002", "Panel Solar EcoTech 550W", 229999.0, 12, 0.23, 550),
        DispositivoEcologico("TER-001", "Termotanque Solar 200L", 320000.0, 8),
    ]
    ruta = GestorInventario.guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
    print(f"Exportación exitosa -> {ruta} ({len(catalogo)} productos)")
