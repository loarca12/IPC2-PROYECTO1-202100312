import xml.etree.ElementTree as ET

class Senal:
    def __init__(self, nombre, t, A):
        self.nombre = nombre
        self.t = t
        self.A = A
        self.datos = []

    def agregar_dato(self, t, A, valor):
        self.datos.append((t, A, valor))

class ProcesadorSenales:
    def __init__(self):
        self.senales = []

    def cargar_archivo(self, ruta):
        try:
            tree = ET.parse(ruta)
            root = tree.getroot()

            for senal_xml in root.findall('senal'):
                nombre = senal_xml.get('nombre')
                t = int(senal_xml.get('t'))
                A = int(senal_xml.get('A'))

                nueva_senal = Senal(nombre, t, A)

                for dato_xml in senal_xml.findall('dato'):
                    t_dato = int(dato_xml.get('t'))
                    A_dato = int(dato_xml.get('A'))
                    valor = int(dato_xml.text)
                    nueva_senal.agregar_dato(t_dato, A_dato, valor)

                self.senales.append(nueva_senal)

            print("Archivo cargado exitosamente.")
        except Exception as e:
            print("Error al cargar el archivo:", e)

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
            print("3. Escribir archivo salida")
            print("4. Mostrar datos del estudiante")
            print("5. Generar gráfica")
            print("6. Inicializar sistema")
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
                self.generar_grafica()
            elif opcion == "6":
                self.inicializar_sistema()
            elif opcion == "7":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    procesador = ProcesadorSenales()
    procesador.mostrar_menu()