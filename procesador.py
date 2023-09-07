import xml.etree.ElementTree as ET  # Herramienta para manipular y parsear XML.
from estructuras import *           # Importa estructuras de datos definidas previamente.
from graphviz import Digraph        # Herramienta para crear gráficos.
import os                           # Biblioteca para manipulación del sistema operativo.


class ProcesadorSenales:
    def __init__(self):
        """Constructor de la clase ProcesadorSenales.
        
        Inicializa una lista de señales.
        """
        self.senales_tda = ListaEnlazadaSenales()

    def cargar_archivo(self, ruta):
        """Carga un archivo XML y crea señales basadas en su contenido."""

        if not ruta.endswith('.xml'):
            print("Error: El archivo debe tener extensión .xml.")
            return
        try:
            tree = ET.parse(ruta)  # Parsea el archivo XML.
            root = tree.getroot()  # Obtiene el elemento raíz del XML.

            # Itera a través de cada señal en el archivo XML.
            for senal_xml in root.findall('senal'):
                nombre = senal_xml.get('nombre')
                nueva_senal = Senal(nombre)

                # Itera sobre cada dato de la señal.
                for dato_xml in senal_xml.findall('dato'):
                    t_dato = int(dato_xml.get('t'))
                    A_dato = int(dato_xml.get('A'))
                    valor = int(dato_xml.text)
                    self.agregar_dato_senal(nueva_senal, t_dato, A_dato, valor)

                # Agrega la señal si no está previamente en la lista.
                if not self.senales_tda.buscar_senal(nombre):
                    self.senales_tda.agregar_senal(nueva_senal)
                    print(f"Señal '{nombre}' agregada.")
                else:
                    print(f"Señal '{nombre}' ya existe. No se agrega.")

            print("Archivo cargado exitosamente.")
        except Exception as e:
            print("Error al cargar el archivo:", e)

    def agregar_dato_senal(self, senal, t, A, valor):
        """Agrega un dato a la señal proporcionada."""
        nuevo_dato = Dato(t, A, valor)
        if not senal.primer_dato:
            senal.primer_dato = nuevo_dato
        else:
            dato_actual = senal.primer_dato
            while dato_actual.siguiente:
                dato_actual = dato_actual.siguiente
            dato_actual.siguiente = nuevo_dato

    def procesar_archivo(self):
        """Procesa las señales cargadas e imprime su nombre."""
        nodo_senal = self.senales_tda.cabeza
        while nodo_senal:
            print(f"Procesando señal {nodo_senal.senal.nombre}...")
            nodo_senal = nodo_senal.siguiente

        print("Procesamiento de archivo finalizado.")

    def escribir_archivo_salida(self):
        """
        Genera y escribe un archivo XML basado en las señales procesadas.

        El archivo contiene las señales divididas en grupos según sus tiempos, 
        y dentro de cada grupo, se describen los datos asociados con tiempos específicos.
        Cada señal en el archivo también incluye un atributo que indica su amplitud máxima.
        """
        try:
            # Solicita al usuario el nombre del archivo de salida (sin extensión).
            nombre_archivo = input("Ingrese el nombre del archivo de salida (sin extensión): ")
            ruta_archivo = nombre_archivo + ".xml"

            # Abre (o crea) el archivo con el nombre especificado para escritura.
            with open(ruta_archivo, "w") as archivo_salida:
                # Escribir etiquetas iniciales del XML.
                archivo_salida.write('<?xml version="1.0"?>\n')
                archivo_salida.write('<senalesReducidas>\n')

                # Itera sobre todas las señales almacenadas en la lista enlazada.
                nodo_senal = self.senales_tda.cabeza
                while nodo_senal:
                    senal = nodo_senal.senal
                    archivo_salida.write(f' <senal nombre="{senal.nombre}" A="{self.get_max_amplitude(senal)}">\n')

                    # Divide la señal en grupos basados en la diferencia de tiempos.
                    grupos = self.divide_into_groups(senal)
                    g = 1
                    while grupos:
                        archivo_salida.write(f'  <grupo g="{g}">\n')

                        # Recopila tiempos únicos dentro del grupo.
                        tiempos = set()
                        dato_actual = grupos.datos
                        while dato_actual:
                            tiempos.add(dato_actual.dato.t)
                            dato_actual = dato_actual.siguiente
                        tiempos_unicos = sorted(list(tiempos))

                        archivo_salida.write(f'   <tiempos>{",".join(map(str, tiempos_unicos))}</tiempos>\n')
                        archivo_salida.write('   <datosGrupo>\n')

                        # Escribe datos asociados a cada tiempo único.
                        for tiempo in tiempos_unicos:
                            dato_actual = grupos.datos
                            while dato_actual:
                                if dato_actual.dato.t == tiempo:
                                    archivo_salida.write(f'    <dato A="{dato_actual.dato.A}">{dato_actual.dato.valor}</dato>\n')
                                dato_actual = dato_actual.siguiente

                        archivo_salida.write('   </datosGrupo>\n')
                        archivo_salida.write('  </grupo>\n')
                        grupos = grupos.siguiente
                        g += 1

                    archivo_salida.write(' </senal>\n')
                    nodo_senal = nodo_senal.siguiente

                archivo_salida.write('</senalesReducidas>\n')

            # Notifica al usuario que el archivo se generó exitosamente.
            print(f"Archivo de salida '{ruta_archivo}' generado exitosamente.")
        except Exception as e:
            # Captura cualquier error que pueda ocurrir e imprime un mensaje.
            print("Error al escribir el archivo de salida:", e)

    def get_max_amplitude(self, senal):
        """
    Obtiene la amplitud máxima de una señal.
    
    Parámetros:
    - senal (objeto): Una instancia que representa una señal con datos asociados.
    
    Devuelve:
    - int: La amplitud máxima encontrada en la señal.

    Método:
    Itera sobre cada dato en la señal. Si la amplitud del dato (dato.A) es mayor que
    la amplitud máxima registrada hasta ese punto, actualiza el valor de la amplitud máxima.
    """
        max_amplitude = 0
        dato = senal.primer_dato
        while dato:
            if dato.A > max_amplitude:
                max_amplitude = dato.A
            dato = dato.siguiente
        return max_amplitude

    def divide_into_groups(self, senal):
        """
    Divide una señal en grupos basados en la diferencia de tiempos entre datos consecutivos.
    
    Parámetros:
    - senal (objeto): Una instancia que representa una señal con datos asociados.
    
    Devuelve:
    - NodoGrupo: La cabeza del primer grupo en la lista enlazada de grupos.

    Método:
    Itera sobre cada dato en la señal. Si el tiempo del dato actual y el último tiempo en el grupo
    actual difieren en 1, se agregan al mismo grupo. Si no, se crea un nuevo grupo.
    """
        cabeza_grupo = NodoGrupo()
        ultimo_grupo = cabeza_grupo

        dato_actual = senal.primer_dato
        while dato_actual:
            if not ultimo_grupo.tiempos.tiempo:  # Si el grupo actual no tiene tiempos
                nuevo_tiempo = NodoTiempo(dato_actual.t)
                ultimo_grupo.tiempos = nuevo_tiempo
                ultimo_grupo.datos = NodoDato(dato_actual)
            else:
                # ultimo tiempo verificaciomn
                ultimo_tiempo = ultimo_grupo.tiempos
                while ultimo_tiempo.siguiente:
                    ultimo_tiempo = ultimo_tiempo.siguiente

                if dato_actual.t - ultimo_tiempo.tiempo == 1:
                    nuevo_tiempo = NodoTiempo(dato_actual.t)
                    ultimo_tiempo.siguiente = nuevo_tiempo
                else:
                    nuevo_grupo = NodoGrupo()
                    nuevo_grupo.tiempos = NodoTiempo(dato_actual.t)
                    nuevo_grupo.datos = NodoDato(dato_actual)
                    ultimo_grupo.siguiente = nuevo_grupo
                    ultimo_grupo = nuevo_grupo

                ultimo_dato = ultimo_grupo.datos
                while ultimo_dato.siguiente:
                    ultimo_dato = ultimo_dato.siguiente
                ultimo_dato.siguiente = NodoDato(dato_actual)

            dato_actual = dato_actual.siguiente

        return cabeza_grupo

    def generar_grafica(self, nombre_senal):
        """
    Genera una gráfica basada en la señal especificada por el nombre.
    
    Parámetros:
    - nombre_senal (str): El nombre de la señal para la cual se desea generar una gráfica.
    
    Método:
    Busca la señal con el nombre especificado en el sistema. Si la señal se encuentra,
    genera y muestra una gráfica. Si no, informa al usuario que la señal no fue encontrada.
    """
        senal = self.senales_tda.buscar_senal(nombre_senal)
        if senal:
            self._graficar_senal(senal)
            print(f"Gráfica para la señal {nombre_senal} generada exitosamente.")
        else:
            print(f"Señal {nombre_senal} no encontrada.")

    def generar_grafica_por_archivo(self, nombre_archivo):
        try:
            # Cargar el archivo
            self.cargar_archivo(nombre_archivo)
            # Generar gráfica para cada señal en el archivo
            nodo_senal = self.senales_tda.cabeza
            while nodo_senal:
                self._graficar_senal(nodo_senal.senal)
                nodo_senal = nodo_senal.siguiente
            print(f"Gráficas generadas exitosamente para el archivo {nombre_archivo}.")
        except Exception as e:
            print(f"Error al generar gráficas para el archivo {nombre_archivo}: {e}")

    def _graficar_senal(self, senal):
        dot = Digraph(comment='Visualización de Señal', format='pdf')
        dot.attr(rankdir='LR')  # Dirección de izquierda a derecha
        dot.attr('node', shape='box')
        
        # datos unicos
        tiempos_unicos = self._obtener_tiempos_unicos(senal)
        amplitudes_unicas = self._obtener_amplitudes_unicas(senal)
        
        nodo_mapa = self._obtener_mapa_datos(senal)
        
        # Crear nodos y conectarlos
        tiempo_actual = tiempos_unicos
        while tiempo_actual:
            t = tiempo_actual.tiempo
            amplitude_actual = amplitudes_unicas
            
            while amplitude_actual:
                A = amplitude_actual.dato
                dato = self._buscar_dato_en_mapa(nodo_mapa, t, A)
                if dato:
                    node_id = f"t{dato.t}_A{dato.A}"
                    label = f"t={dato.t}\nA={dato.A}\nF={dato.valor}"  
                    dot.node(node_id, label=label)

                    # Conectar nodos horizontalmente
                    if tiempo_actual.siguiente:  # Si no es el último tiempo
                        next_node_id = f"t{tiempo_actual.siguiente.tiempo}_A{A}"
                        dot.edge(node_id, next_node_id, dir="both")

                    # Conectar nodos verticalmente
                    if amplitude_actual.siguiente:  # Si no es la última amplitude
                        lower_node_id = f"t{t}_A{amplitude_actual.siguiente.dato}"
                        dot.edge(node_id, lower_node_id, dir="both")
                
                amplitude_actual = amplitude_actual.siguiente
            
            tiempo_actual = tiempo_actual.siguiente

        # Crear el directorio si no existe
        if not os.path.exists('graficas'):
            os.makedirs('graficas')

        dot.render(f"graficas/{senal.nombre}", format="pdf", cleanup=True, view=True)
        dot.save(filename=f"graficas/{senal.nombre}.gv")

    def _obtener_tiempos_unicos(self, senal):
        """
    Obtiene una lista enlazada de tiempos únicos presentes en una señal.

    Parámetros:
    - senal (objeto): Una instancia que representa una señal con datos asociados.

    Devuelve:
    - NodoTiempo: La cabeza del primer tiempo en la lista enlazada de tiempos únicos.

    Método:
    Itera sobre cada dato en la señal. Si el tiempo del dato actual no está ya en la lista,
    se añade a la lista enlazada de tiempos únicos.
    """
        tiempos = NodoTiempo()
        ultimo_tiempo = tiempos

        dato_actual = senal.primer_dato
        while dato_actual:
            if not self._tiempo_existe(tiempos, dato_actual.t):
                if ultimo_tiempo.tiempo:
                    nuevo_tiempo = NodoTiempo(dato_actual.t)
                    ultimo_tiempo.siguiente = nuevo_tiempo
                    ultimo_tiempo = nuevo_tiempo
                else:
                    ultimo_tiempo.tiempo = dato_actual.t
            
            dato_actual = dato_actual.siguiente

        return tiempos

    def _obtener_amplitudes_unicas(self, senal):
        """
    Obtiene una lista enlazada de amplitudes únicas presentes en una señal.

    Parámetros:
    - senal (objeto): Una instancia que representa una señal con datos asociados.

    Devuelve:
    - NodoDato: La cabeza del primer dato (amplitude) en la lista enlazada de amplitudes únicas.

    Método:
    Itera sobre cada dato en la señal. Si la amplitude del dato actual no está ya en la lista,
    se añade a la lista enlazada de amplitudes únicas.
    """
        amplitudes = NodoDato()
        ultima_amplitude = amplitudes

        dato_actual = senal.primer_dato
        while dato_actual:
            if not self._amplitude_existe(amplitudes, dato_actual.A):
                if ultima_amplitude.dato:
                    nueva_amplitude = NodoDato(dato_actual.A)
                    ultima_amplitude.siguiente = nueva_amplitude
                    ultima_amplitude = nueva_amplitude
                else:
                    ultima_amplitude.dato = dato_actual.A

            dato_actual = dato_actual.siguiente

        return amplitudes

    def _obtener_mapa_datos(self, senal):
        """
    Crea una lista enlazada que mapea cada dato de una señal.

    Parámetros:
    - senal (objeto): Una instancia que representa una señal con datos asociados.

    Devuelve:
    - NodoMapa: La cabeza del primer nodo en la lista enlazada que representa el mapa de datos.

    Método:
    Itera sobre cada dato en la señal, y crea un nuevo nodo mapa para cada dato. Cada nodo mapa
    contiene el tiempo, la amplitude y una referencia al dato original.
    """
        cabeza_mapa = NodoMapa(None, None, None)
        ultimo_nodo = cabeza_mapa

        dato_actual = senal.primer_dato
        while dato_actual:
            nuevo_nodo = NodoMapa(dato_actual.t, dato_actual.A, dato_actual)
            ultimo_nodo.siguiente = nuevo_nodo
            ultimo_nodo = nuevo_nodo
            dato_actual = dato_actual.siguiente

        return cabeza_mapa.siguiente

    def _tiempo_existe(self, tiempos, tiempo):
        """
    Verifica si un tiempo específico ya existe en la lista enlazada de tiempos.

    Parámetros:
    - tiempos (NodoTiempo): La cabeza del primer nodo en la lista enlazada de tiempos.
    - tiempo (float/int): El valor del tiempo que se desea verificar.

    Devuelve:
    - bool: True si el tiempo ya existe en la lista, False en caso contrario.

    Método:
    Itera sobre la lista enlazada de tiempos. Si encuentra un nodo con el mismo valor 
    que el tiempo proporcionado, devuelve True. Si no encuentra coincidencias, devuelve False.
    """
        tiempo_actual = tiempos
        while tiempo_actual:
            if tiempo_actual.tiempo == tiempo:
                return True
            tiempo_actual = tiempo_actual.siguiente
        return False

    def _amplitude_existe(self, amplitudes, amplitude):
        """
    Verifica si una amplitud específica ya existe en la lista enlazada de amplitudes.

    Parámetros:
    - amplitudes (NodoDato): La cabeza del primer dato en la lista enlazada de amplitudes.
    - amplitude (float/int): El valor de la amplitud que se desea verificar.

    Devuelve:
    - bool: True si la amplitud ya existe en la lista, False en caso contrario.

    Método:
    Itera sobre la lista enlazada de amplitudes. Si encuentra un nodo con el mismo valor 
    que la amplitud proporcionada, devuelve True. Si no encuentra coincidencias, devuelve False.
    """
        amplitude_actual = amplitudes
        while amplitude_actual:
            if amplitude_actual.dato == amplitude:
                return True
            amplitude_actual = amplitude_actual.siguiente
        return False
    
    def _buscar_dato_en_mapa(self, nodo_mapa, t, A):
        """
    Busca un dato específico en la lista enlazada de mapas basándose en un tiempo y una amplitud.

    Parámetros:
    - nodo_mapa (NodoMapa): La cabeza del primer nodo en la lista enlazada que representa el mapa de datos.
    - t (float/int): El valor del tiempo asociado al dato que se busca.
    - A (float/int): El valor de la amplitud asociada al dato que se busca.

    Devuelve:
    - objeto: El dato encontrado que coincide con el tiempo y la amplitud proporcionados, o None si no se encuentra.

    Método:
    Itera sobre la lista enlazada de mapas de datos. Si encuentra un nodo que coincide con 
    el tiempo y la amplitud proporcionados, devuelve el dato asociado. Si no encuentra coincidencias, devuelve None.
    """
        while nodo_mapa:
            if nodo_mapa.t == t and nodo_mapa.A == A:
                return nodo_mapa.dato
            nodo_mapa = nodo_mapa.siguiente
        return None
    
    def reiniciar_sistema(self):
        """Reinicia la lista de señales y limpia cualquier dato cargado."""
        self.senales_tda = ListaEnlazadaSenales()
        print("Sistema reiniciado exitosamente.")

    def mostrar_datos_estudiante(self):

        datos_estudiante = """
Nombre: Giancarlo Adonay Cifuentes Loarca
Carné: 202100312
Curso: Introduccion a la programacion y computacion seccion \"N\"
Carrera: Ingenieria en ciencias y sistemas
Semestre: Sexto semestre
        """
        print(datos_estudiante)

    def mostrar_menu(self):
        while True:
            print("=====================================")
            print("Menú principal:")
            print("1. Cargar archivo")
            print("2. Procesar archivo")
            print("3. Escribir archivo de salida")
            print("4. Mostrar datos del estudiante")
            print("5. Generar gráfica")
            print("6. Reiniciar sistema")
            print("7. Salida")
            print("=====================================")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                ruta = input("Ingrese la ruta del archivo XML: ")
                self.cargar_archivo(ruta)
            elif opcion == "2":
                self.procesar_archivo()
            elif opcion == "3":
                self.escribir_archivo_salida()
            elif opcion == "4":
                self.mostrar_datos_estudiante()
            elif opcion == "5":
                nombre_archivo = input("Ingrese el nombre del archivo para generar las gráficas: ")
                self.generar_grafica_por_archivo(nombre_archivo)
            elif opcion == "6":
                self.reiniciar_sistema()
            elif opcion == "7":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

