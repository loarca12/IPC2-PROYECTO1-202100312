# Definición de la clase NodoGrupo
class NodoGrupo:
    def __init__(self):
        # Atributos de NodoGrupo
        # tiempos: Un objeto de tipo NodoTiempo para almacenar información relacionada con tiempos.
        self.tiempos = NodoTiempo()
        # datos: Un objeto de tipo NodoDato para almacenar información relacionada con datos.
        self.datos = NodoDato()
        # siguiente: Una referencia al siguiente nodo en la lista.
        self.siguiente = None

# Definición de la clase NodoTiempo
class NodoTiempo:
    def __init__(self, tiempo=None):
        # Atributos de NodoTiempo
        # tiempo: Un valor de tiempo opcional.
        self.tiempo = tiempo
        # siguiente: Una referencia al siguiente nodo en la lista de tiempos.
        self.siguiente = None

# Definición de la clase NodoDato
class NodoDato:
    def __init__(self, dato=None):
        # Atributos de NodoDato
        # dato: Un valor de dato opcional.
        self.dato = dato
        # siguiente: Una referencia al siguiente nodo en la lista de datos.
        self.siguiente = None

# Definición de la clase Dato
class Dato:
    def __init__(self, t, A, valor):
        # Atributos de Dato
        # t: Tiempo.
        self.t = t
        # A: Amplitud.
        self.A = A
        # valor: Valor asociado a los datos.
        self.valor = valor
        # siguiente: Una referencia al siguiente dato en la lista de datos.
        self.siguiente = None

# Definición de la clase Senal
class Senal:
    def __init__(self, nombre):
        # Atributos de Senal
        # nombre: Nombre de la señal.
        self.nombre = nombre
        # primer_dato: Referencia al primer dato relacionado con la señal.
        self.primer_dato = None

# Definición de la clase NodoSenal
class NodoSenal:
    def __init__(self, senal):
        # Atributos de NodoSenal
        # senal: Un objeto de tipo Senal que representa una señal.
        self.senal = senal
        # siguiente: Una referencia al siguiente nodo en la lista de señales.
        self.siguiente = None

# Definición de la clase ListaEnlazadaSenales
class ListaEnlazadaSenales:
    def __init__(self):
        # Atributos de ListaEnlazadaSenales
        # cabeza: Referencia al primer nodo de señal en la lista.
        self.cabeza = None       

    # Método para agregar una señal al principio de la lista de señales
    def agregar_senal(self, senal):
        nuevo_nodo = NodoSenal(senal)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo

    # Método para buscar una señal por nombre en la lista de señales
    def buscar_senal(self, nombre):
        nodo_actual = self.cabeza
        while nodo_actual:
            if nodo_actual.senal.nombre == nombre:
                return nodo_actual.senal
            nodo_actual = nodo_actual.siguiente
        return None

# Definición de la clase NodoMapa
class NodoMapa:
    def __init__(self, t, A, dato):
        # Atributos de NodoMapa
        # t: Tiempo.
        self.t = t
        # A: Amplitud.
        self.A = A
        # dato: Valor de dato asociado.
        self.dato = dato
        # siguiente: Una referencia al siguiente nodo en la estructura de datos.
        self.siguiente = None
