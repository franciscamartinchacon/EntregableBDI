#MENU PRINCIPAL

def menu():
    while True:
        print("\n--- Sistema de Actividades Deportivas ---")
        print("1. ABM estudiantes")
        print("2. ABM disciplinas deportivas")
        print("3. ABM espacios deportivos")
        print("4. ABM actividades deportivas")
        print("5. Inscribir estudiante")
        print("6. Registrar asistencia")
        print("7. Consultar reportes")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ABM_estudiantes()
        elif opcion == "2":
            ABM_disciplinas()
        elif opcion == "3":
            ABM_espacios_deportivos()
        elif opcion == "4":
            ABM_actividades_deportivas()
        elif opcion == "5":
            gestion_inscripciones()
        elif opcion == "6":
            registrar_asistencia()
        elif opcion == "7":
            reportes()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")


#SOLO PARA QUE NO DE ERROR, NO SE USAN ESTAS!! ARREGLAR
def ABM_estudiantes():
    while True:
        print()

def ABM_disciplinas():
    while True:
        print()
def ABM_espacios_deportivos():
    while True:
        print()
def ABM_actividades_deportivas():
    while True:
        print()
def gestion_inscripciones():
    while True:
        print()
def registrar_asistencia():
    while True:
        print()
def  reportes():
    while True:
        print()
menu()