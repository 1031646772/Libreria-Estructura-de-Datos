# core/lista_lineal.py
# Implementación de Lista Lineal (Lista Enlazada Simple)

#Se define la clase Nodo
class Nodo:
    #Constructor de Nodo
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

#Se define la clase ListaLineal

class ListaLineal:
    
    #Lista Lineal (Enlazada Simple).
    #insertar, eliminar, buscar, listar y longitud.
    

    def __init__(self):
        self.cabeza = None
        self._longitud = 0

    # Inserción
    #Define un método que recibe un dato y lo inserta en la lista. No retorna nada (None).
    def insertar(self, dato) -> None:
        #Inserta un elemento al final de la lista.
        nuevo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente: #Itera mientras haya nodos en la lista.
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._longitud += 1


    # Eliminación
    #Define un método que recibe una función criterio y devuelve True si se eliminó un nodo, False si no se encontró.
    def eliminar(self, criterio) -> bool:
      
        #Elimina el primer nodo cuyo dato satisface criterio(dato) == True.
        #Retorna True si se eliminó, False si no se encontró.

        actual = self.cabeza #Inicializa dos punteros:
        anterior = None
        while actual: #Itera mientras haya nodos en la lista.
            if criterio(actual.dato):
                if anterior is None: #Si el nodo a eliminar es la cabeza, se actualiza la cabeza al siguiente nodo.
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self._longitud -= 1 #Reduce la longitud de la lista en 1, porque se eliminó un nodo.
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    # Búsqueda

    def buscar(self, criterio):
        #Retorna el primer dato que satisface criterio(dato) == True, o None si no existe. 
        actual = self.cabeza
        while actual:
            if criterio(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    def buscar_todos(self, criterio) -> list:
        #Retorna todos los datos que satisfacen el criterio.
        resultado = [] #Definicion de arreglo resultado
        actual = self.cabeza
        while actual:
            if criterio(actual.dato):
                resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado


    # Listado
    #Define un método que retorna una lista de Python con los datos almacenados.
    def listar(self) -> list:
        #Retorna todos los datos como lista de Python.
        resultado = []
        actual = self.cabeza #Empieza desde el primer nodo de la lista enlazada.
        while actual: #Recorre la lista mientras haya nodos.
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado


    # Propiedades

    def esta_vacia(self) -> bool:
        return self.cabeza is None

    def __len__(self) -> int:
        return self._longitud

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente
