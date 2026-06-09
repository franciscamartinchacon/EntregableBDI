#ABM disciplinas
#depliega otro menu [agregar, borrar, modificar, disciplinas]

def ABM_disciplinas():
    while True:
        print("\n--- ABM disciplinas ---")
        print("1. Agregar disciplina")
        print("2. Borrar disciplina")
        print("3. Actualizar disciplina")
        print("4. Volver al menú principal")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_disciplina()
        elif opcion == "2":
            borrar_disciplina()
        elif opcion == "3":
            actualizar_disciplina()
        elif opcion == "4":
            menu()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")


def agregar_disciplina():
    while True:


