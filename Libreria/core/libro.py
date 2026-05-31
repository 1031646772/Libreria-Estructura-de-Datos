# core/libro.py

class Libro:
    #Se define el contructor de Libro para ingresar sus atributos

    def __init__(self, isbn: str, titulo: str, autor: str, anio: int, cantidad: int = 1):
        self.isbn = isbn.strip()
        self.titulo = titulo.strip()
        self.autor = autor.strip()
        self.anio = int(anio)
        self.cantidad = int(cantidad)         #Referencia la cantidad total
        self.disponibles = int(cantidad)       # Referencia los disponibles de la cantidad total

   
    # Prestar libro
    
    #Se definen las funciones prestar y devolver retornaran un valor booleano 
    def prestar(self) -> bool:
        #Descuenta un libro disponible. Retorna True si se pudo prestar
        if self.disponibles > 0:
            self.disponibles -= 1
            return True
        return False

    def devolver(self) -> bool:
        # Incrementa los disponibles al devolver. Retorna True si era válido.
        if self.disponibles < self.cantidad:
            self.disponibles += 1
            return True
        return False

    # Representación
    
    def __str__(self) -> str:
        return (
            #Devuelve una cadena formateada con los atributos principales del libro
            f"[{self.isbn}] {self.titulo} — {self.autor} "
            f"({self.anio})  Disp: {self.disponibles}/{self.cantidad}"
        )

    def to_dict(self) -> dict:
        #Devuelve un diccionario con las claves y valores:
        return {
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "anio": self.anio,
            "cantidad": self.cantidad,
            "disponibles": self.disponibles,
        }
