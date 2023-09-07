# Importa la clase ProcesadorSenales del módulo procesador.
from procesador import ProcesadorSenales

# Verifica si el script se está ejecutando como el programa principal.
if __name__ == "__main__":
    # Crea una instancia de la clase ProcesadorSenales.
    procesador = ProcesadorSenales()

    # Inicia el menú principal del procesador de señales.
    procesador.mostrar_menu()