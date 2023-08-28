import xml.etree.ElementTree as ET
from estructuras import *

class ProcesadorSenales:
    def __init__(self):
        self.senales_tda = ListaEnlazadaSenales()
class ProcesadorSenales:
    def __init__(self):
        self.senales_tda = ListaEnlazadaSenales()

    def cargar_archivo(self, ruta):
        try:
            tree = ET.parse(ruta)
            root = tree.getroot()

            for senal_xml in root.findall('senal'):
                nombre = senal_xml.get('nombre')

                nueva_senal = Senal(nombre)

                for dato_xml in senal_xml.findall('dato'):
                    t_dato = int(dato_xml.get('t'))
                    A_dato = int(dato_xml.get('A'))
                    valor = int(dato_xml.text)
                    self.agregar_dato_senal(nueva_senal, t_dato, A_dato, valor)

                if not self.senales_tda.buscar_senal(nombre):
                    self.senales_tda.agregar_senal(nueva_senal)
                    print(f"Señal '{nombre}' agregada.")
                else:
                    print(f"Señal '{nombre}' ya existe. No se agrega.")

            print("Archivo cargado exitosamente.")
        except Exception as e:
            print("Error al cargar el archivo:", e)

    def agregar_dato_senal(self, senal, t, A, valor):
        nuevo_dato = Dato(t, A, valor)
        if not senal.primer_dato:
            senal.primer_dato = nuevo_dato
        else:
            dato_actual = senal.primer_dato
            while dato_actual.siguiente:
                dato_actual = dato_actual.siguiente
            dato_actual.siguiente = nuevo_dato

    def procesar_archivo(self):
        nodo_senal = self.senales_tda.cabeza
        while nodo_senal:
            print(f"Procesando señal {nodo_senal.senal.nombre}...")
            nodo_senal = nodo_senal.siguiente

        print("Procesamiento de archivo finalizado.")

    def escribir_archivo_salida(self):
        try:
            nombre_archivo = input("Ingrese el nombre del archivo de salida (sin extensión): ")
            ruta_archivo = nombre_archivo + ".xml"

            with open(ruta_archivo, "w") as archivo_salida:
                archivo_salida.write('<?xml version="1.0"?>\n')
                archivo_salida.write('<senalesReducidas>\n')

                nodo_senal = self.senales_tda.cabeza
                while nodo_senal:
                    senal = nodo_senal.senal
                    archivo_salida.write(f' <senal nombre="{senal.nombre}" A="{self.get_max_amplitude(senal)}">\n')
                    
                    grupo_actual = self.divide_into_groups(senal)
                    g = 1
                    while grupo_actual:
                        archivo_salida.write(f' <grupo g={g}>\n')

                        archivo_salida.write(' <tiempos>')
                        tiempo_actual = grupo_actual.tiempos
                        first = True
                        while tiempo_actual:
                            if not first:
                                archivo_salida.write(',')
                            else:
                                first = False
                            archivo_salida.write(str(tiempo_actual.tiempo))
                            tiempo_actual = tiempo_actual.siguiente
                        archivo_salida.write('</tiempos>\n')

                        archivo_salida.write(' <datosGrupo>\n')
                        dato_actual = grupo_actual.datos
                        while dato_actual:
                            archivo_salida.write(f' <dato A={dato_actual.dato.A}>{dato_actual.dato.valor}</dato>\n')
                            dato_actual = dato_actual.siguiente
                        archivo_salida.write(' </datosGrupo>\n')
                        
                        archivo_salida.write(' </grupo>\n')
                        grupo_actual = grupo_actual.siguiente
                        g += 1

                    archivo_salida.write(' </senal>\n')
                    nodo_senal = nodo_senal.siguiente

                archivo_salida.write('</senalesReducidas>\n')

            print(f"Archivo de salida '{ruta_archivo}' generado exitosamente.")
        except Exception as e:
            print("Error al escribir el archivo de salida:", e)


    def get_max_amplitude(self, senal):
        max_amplitude = 0
        dato = senal.primer_dato
        while dato:
            if dato.A > max_amplitude:
                max_amplitude = dato.A
            dato = dato.siguiente
        return max_amplitude

    def divide_into_groups(self, senal):
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
            print("6. Salida")
            print("=====================================")

            opcion = input("Seleccione una opción: ")
            # implemnetacion de la grafica falta
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
                nombre_senal = input("Ingrese el nombre de la señal de audio que desea visualizar: ")
                self.generar_grafica(nombre_senal)
            elif opcion == "6":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

