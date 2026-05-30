# core/libro.py
print("funcionando rama")

class Libro:
    """Modelo de dominio para un libro."""

    def __init__(self, isbn: str, titulo: str, autor: str, anio: int, cantidad: int = 1):
        self.isbn = isbn.strip()
        self.titulo = titulo.strip()
        self.autor = autor.strip()
        self.anio = int(anio)
        self.cantidad = int(cantidad)          # ejemplares totales
        self.disponibles = int(cantidad)       # ejemplares disponibles

    # ──────────────────────────────────────────────
    # Préstamo
    # ──────────────────────────────────────────────
    def prestar(self) -> bool:
        """Descuenta un ejemplar disponible. Retorna True si se pudo prestar."""
        if self.disponibles > 0:
            self.disponibles -= 1
            return True
        return False

    def devolver(self) -> bool:
        """Incrementa los disponibles al devolver. Retorna True si era válido."""
        if self.disponibles < self.cantidad:
            self.disponibles += 1
            return True
        return False

    # ──────────────────────────────────────────────
    # Representación
    # ──────────────────────────────────────────────
    def __str__(self) -> str:
        return (
            f"[{self.isbn}] {self.titulo} — {self.autor} "
            f"({self.anio})  Disp: {self.disponibles}/{self.cantidad}"
        )

    def to_dict(self) -> dict:
        return {
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "anio": self.anio,
            "cantidad": self.cantidad,
            "disponibles": self.disponibles,
        }
