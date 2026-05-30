# core/libreria_service.py
# Capa de lógica de negocio.  La UI solo llama a estas funciones.

from core.lista_lineal import ListaLineal
from core.libro import Libro
from core.usuario import Usuario


class LibreriaService:
    """
    Servicio central que gestiona libros, usuarios y préstamos
    usando Listas Lineales como estructura de datos.
    """

    def __init__(self):
        self._libros: ListaLineal = ListaLineal()
        self._usuarios: ListaLineal = ListaLineal()
        self._prestamos: ListaLineal = ListaLineal()  # cada nodo: (cedula, isbn)
        self._cargar_datos_demo()

    # ══════════════════════════════════════════════
    # LIBROS
    # ══════════════════════════════════════════════

    def ingresar_libro(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        anio: int,
        cantidad: int = 1,
    ) -> tuple[bool, str]:
        """
        Registra un nuevo libro.
        Retorna (éxito: bool, mensaje: str).
        """
        if not isbn or not titulo or not autor:
            return False, "ISBN, título y autor son obligatorios."

        existe = self._libros.buscar(lambda l: l.isbn == isbn)
        if existe:
            return False, f"Ya existe un libro con ISBN '{isbn}'."

        try:
            libro = Libro(isbn, titulo, autor, anio, cantidad)
        except ValueError as e:
            return False, f"Datos inválidos: {e}"

        self._libros.insertar(libro)
        return True, f"Libro '{titulo}' registrado correctamente."

    def listar_libros(self) -> list[Libro]:
        """Retorna todos los libros registrados."""
        return self._libros.listar()

    def buscar_libro(self, isbn: str):
        """Busca y retorna un Libro por ISBN, o None."""
        return self._libros.buscar(lambda l: l.isbn == isbn)

    # ══════════════════════════════════════════════
    # USUARIOS
    # ══════════════════════════════════════════════

    def ingresar_usuario(
        self,
        cedula: str,
        nombre: str,
        email: str,
    ) -> tuple[bool, str]:
        """
        Registra un nuevo usuario.
        Retorna (éxito: bool, mensaje: str).
        """
        if not cedula or not nombre or not email:
            return False, "Cédula, nombre y email son obligatorios."

        existe = self._usuarios.buscar(lambda u: u.cedula == cedula)
        if existe:
            return False, f"Ya existe un usuario con cédula '{cedula}'."

        usuario = Usuario(cedula, nombre, email)
        self._usuarios.insertar(usuario)
        return True, f"Usuario '{nombre}' registrado correctamente."

    def listar_usuarios(self) -> list[Usuario]:
        """Retorna todos los usuarios registrados."""
        return self._usuarios.listar()

    def buscar_usuario(self, cedula: str):
        """Busca y retorna un Usuario por cédula, o None."""
        return self._usuarios.buscar(lambda u: u.cedula == cedula)

    # ══════════════════════════════════════════════
    # PRÉSTAMOS
    # ══════════════════════════════════════════════

    def prestar_libro(self, cedula: str, isbn: str) -> tuple[bool, str]:
        """
        Registra el préstamo de un libro a un usuario.
        Retorna (éxito: bool, mensaje: str).
        """
        usuario = self.buscar_usuario(cedula)
        if not usuario:
            return False, f"No se encontró el usuario con cédula '{cedula}'."

        libro = self.buscar_libro(isbn)
        if not libro:
            return False, f"No se encontró el libro con ISBN '{isbn}'."

        if not libro.prestar():
            return False, (
                f"No hay ejemplares disponibles de '{libro.titulo}'. "
                f"Disponibles: {libro.disponibles}/{libro.cantidad}."
            )

        usuario.agregar_prestamo(isbn)
        self._prestamos.insertar({"cedula": cedula, "isbn": isbn})
        return True, (
            f"Préstamo exitoso: '{libro.titulo}' → {usuario.nombre}. "
            f"Disponibles restantes: {libro.disponibles}/{libro.cantidad}."
        )

    def devolver_libro(self, cedula: str, isbn: str) -> tuple[bool, str]:
        """
        Registra la devolución de un libro.
        Retorna (éxito: bool, mensaje: str).
        """
        usuario = self.buscar_usuario(cedula)
        if not usuario:
            return False, f"No se encontró el usuario con cédula '{cedula}'."

        libro = self.buscar_libro(isbn)
        if not libro:
            return False, f"No se encontró el libro con ISBN '{isbn}'."

        if not usuario.tiene_libro(isbn):
            return False, f"El usuario no tiene prestado el libro '{isbn}'."

        usuario.remover_prestamo(isbn)
        libro.devolver()

        # Eliminar registro de préstamo
        self._prestamos.eliminar(
            lambda p: p["cedula"] == cedula and p["isbn"] == isbn
        )
        return True, f"Devolución exitosa: '{libro.titulo}' devuelto por {usuario.nombre}."

    def listar_prestamos(self) -> list[dict]:
        """Retorna todos los préstamos activos como lista de dicts."""
        return self._prestamos.listar()

    # ══════════════════════════════════════════════
    # DATOS DEMO
    # ══════════════════════════════════════════════

    def _cargar_datos_demo(self) -> None:
        """Carga datos de ejemplo para facilitar la demostración."""
        self.ingresar_libro("978-0-06-112008-4", "To Kill a Mockingbird", "Harper Lee", 1960, 3)
        self.ingresar_libro("978-0-7432-7356-5", "1984", "George Orwell", 1949, 2)
        self.ingresar_libro("978-0-14-028329-7", "El Principito", "Antoine de Saint-Exupéry", 1943, 4)
        self.ingresar_libro("978-0-06-093546-9", "Cien Años de Soledad", "Gabriel García Márquez", 1967, 2)

        self.ingresar_usuario("1001", "María López", "maria@email.com")
        self.ingresar_usuario("1002", "Carlos Ruiz", "carlos@email.com")
        self.ingresar_usuario("1003", "Ana Torres", "ana@email.com")

