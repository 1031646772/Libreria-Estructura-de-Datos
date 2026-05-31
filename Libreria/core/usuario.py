# core/usuario.py

#Definicion de Clase Usuario

class Usuario:
    #Modelo de dominio para un usuario de la librería.
    #Constructor usuario
    def __init__(self, cedula: str, nombre: str, email: str):
        self.cedula = cedula.strip()
        self.nombre = nombre.strip()
        self.email = email.strip()
        self.libros_prestados: list = []    # lista de ISBN prestados

    # Préstamo
    #Define un método que recibe el ISBN de un libro y no retorna nada (None).
    def agregar_prestamo(self, isbn: str) -> None:
        self.libros_prestados.append(isbn) #Agrega el ISBN del libro a la lista libros_prestados del usuario, registrando que ese libro está actualmente prestado por él.

    def remover_prestamo(self, isbn: str) -> bool:
        if isbn in self.libros_prestados:
            self.libros_prestados.remove(isbn)
            return True
        return False

    def tiene_libro(self, isbn: str) -> bool:
        return isbn in self.libros_prestados

    # Representación

    def __str__(self) -> str:
        prestados = len(self.libros_prestados)
        return (
            f"[{self.cedula}] {self.nombre} — {self.email}  "
            f"Préstamos activos: {prestados}"
        )
    #Define un método que devuelve un diccionario con la información del usuario.
    def to_dict(self) -> dict:
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "email": self.email,
            "libros_prestados": self.libros_prestados,
        }
