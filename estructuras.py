class NodoGrupo:
    def __init__(self):
        self.tiempos = NodoTiempo()
        self.datos = NodoDato()
        self.siguiente = None

class NodoTiempo:
    def __init__(self, tiempo=None):
        self.tiempo = tiempo
        self.siguiente = None

class NodoDato:
    def __init__(self, dato=None):
        self.dato = dato
        self.siguiente = None

class Dato:
    def __init__(self, t, A, valor):
        self.t = t
        self.A = A
        self.valor = valor
        self.siguiente = None

class Senal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.primer_dato = None

class NodoSenal:
    def __init__(self, senal):
        self.senal = senal
        self.siguiente = None

class ListaEnlazadaSenales:
    def __init__(self):
        self.cabeza = None       

    def agregar_senal(self, senal):
        nuevo_nodo = NodoSenal(senal)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo

    def buscar_senal(self, nombre):
        nodo_actual = self.cabeza
        while nodo_actual:
            if nodo_actual.senal.nombre == nombre:
                return nodo_actual.senal
            nodo_actual = nodo_actual.siguiente
        return None
