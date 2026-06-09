#MENU

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
            gestión_inscripciones()
        elif opcion == "6":
            registrar_asistencia()
        elif opcion == "7":
            reportes()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")

def ABM_estudiantes():
    while True:
        print()

#def ABM_disciplinas():

def ABM_espacios_deportivos():

def ABM_actividades_deportivas():

def gestión_inscripciones():

def registrar_asistencia():

def  reportes():

menu()