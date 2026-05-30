# core/lista_lineal.py
# Implementación de Lista Lineal (Lista Enlazada Simple)


class Nodo:
    """Nodo de la lista lineal."""
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaLineal:
    """
    Lista Lineal (Enlazada Simple).
    Soporta: insertar, eliminar, buscar, listar y longitud.
    """

    def __init__(self):
        self.cabeza = None
        self._longitud = 0

    # ──────────────────────────────────────────────
    # Inserción
    # ──────────────────────────────────────────────
    def insertar(self, dato) -> None:
        """Inserta un elemento al final de la lista."""
        nuevo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._longitud += 1

    # ──────────────────────────────────────────────
    # Eliminación
    # ──────────────────────────────────────────────
    def eliminar(self, criterio) -> bool:
        """
        Elimina el primer nodo cuyo dato satisface criterio(dato) == True.
        Retorna True si se eliminó, False si no se encontró.
        """
        actual = self.cabeza
        anterior = None
        while actual:
            if criterio(actual.dato):
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self._longitud -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    # ──────────────────────────────────────────────
    # Búsqueda
    # ──────────────────────────────────────────────
    def buscar(self, criterio):
        """
        Retorna el primer dato que satisface criterio(dato) == True,
        o None si no existe.
        """
        actual = self.cabeza
        while actual:
            if criterio(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    def buscar_todos(self, criterio) -> list:
        """Retorna todos los datos que satisfacen el criterio."""
        resultado = []
        actual = self.cabeza
        while actual:
            if criterio(actual.dato):
                resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    # ──────────────────────────────────────────────
    # Listado
    # ──────────────────────────────────────────────
    def listar(self) -> list:
        """Retorna todos los datos como lista de Python."""
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    # ──────────────────────────────────────────────
    # Propiedades
    # ──────────────────────────────────────────────
    def esta_vacia(self) -> bool:
        return self.cabeza is None

    def __len__(self) -> int:
        return self._longitud

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente
