"""Ejercicio 2 - Modelo de Productos, Excepciones y Persistencia (40 pts)."""
import json

class StockInvalidoError(ValueError):
    """Se eleva cuando se intenta asignar un stock negativo."""
    pass

class DispositivoEcologico:
    """Clase base. Encapsulamiento explícito del stock vía property."""
    def __init__(self, nombre: str, precio: float, stock: int):
        self.nombre = nombre.strip()
        self.precio = float(precio)
        self._stock = None
        self.stock = stock  # pasa por el setter validado

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise StockInvalidoError(f"El stock debe ser un entero, se recibió {valor!r}")
        if valor < 0:
            raise StockInvalidoError(f"El stock no puede ser negativo: {valor}")
        self._stock = valor

    def ficha_tecnica(self) -> str:
        return f"{self.nombre} | Precio: ${self.precio:,.2f} | Stock: {self.stock}"

    def to_dict(self) -> dict:
        return {"tipo": type(self).__name__, "nombre": self.nombre, "precio": self.precio, "stock": self.stock}

    def __repr__(self):
        return f"{type(self).__name__}(nombre={self.nombre!r}, precio={self.precio}, stock={self.stock})"

class PanelSolar(DispositivoEcologico):
    """Especialización con atributos propios y polimorfismo en ficha_tecnica."""
    def __init__(self, nombre: str, precio: float, stock: int, potencia_w: int, eficiencia: float):
        super().__init__(nombre, precio, stock)
        self.potencia_w = int(potencia_w)
        self.eficiencia = float(eficiencia)  # ej. 0.22 = 22%

    # Polimorfismo: personaliza la ficha
    def ficha_tecnica(self) -> str:
        base = super().ficha_tecnica()
        return f"{base} | Panel Solar {self.potencia_w}W | Eficiencia: {self.eficiencia*100:.1f}%"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"potencia_w": self.potencia_w, "eficiencia": self.eficiencia})
        return d

class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo: str = "catalogo_ecotech.json") -> str:
        datos = [d.to_dict() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return ruta_archivo

    @staticmethod
    def cargar_catalogo_json(ruta_archivo: str = "catalogo_ecotech.json"):
        with open(ruta_archivo, encoding="utf-8") as f:
            return json.load(f)

if __name__ == "__main__":
    catalogo = []
    # 1) Captura controlada de StockInvalidoError
    try:
        panel_invalido = PanelSolar("Panel X", 150000, -5, 450, 0.21)
        catalogo.append(panel_invalido)
    except StockInvalidoError as e:
        print(f"[OK] StockInvalidoError capturado: {e}")

    # 2) Productos válidos
    catalogo.append(PanelSolar("Panel Solar EcoTech 450W", 189999.0, 25, 450, 0.22))
    catalogo.append(PanelSolar("Panel Solar EcoTech 550W", 229999.0, 12, 550, 0.23))
    catalogo.append(DispositivoEcologico("Termotanque Solar 200L", 320000.0, 8))

    for p in catalogo:
        print(p.ficha_tecnica())

    ruta = GestorInventario.guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
    print(f"\nExportación exitosa -> {ruta} ({len(catalogo)} productos)")
