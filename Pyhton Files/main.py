from estudiantes import menu_estudiantes
from disciplinas import menu_disciplinas
from espacios import menu_espacios
from actividades import menu_actividades
from inscripciones import gestion_inscripciones
from asistencias import menu_asistencias
from reportes import menu_reportes
from usuario import login

def inicio():
    while True:
        usuario = login()
        if usuario is None:
            print("Usuario o contraseña invalidos. Intnte nuevamente. ")
            continue

    documento = usuario[0]
    rol = usuario[1]

    print(f"\nHas iniciado seción {rol}")
    if rol == "admin":
        menu_admin()

    elif rol == "docente":
        menu_docente()

    elif rol == "estudiante":
        menu_estudiante()
    return


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
            menu_estudiantes()
        elif opcion == "2":
            menu_disciplinas()
        elif opcion == "3":
            menu_espacios()
        elif opcion == "4":
            menu_actividades()
        elif opcion == "5":
            gestion_inscripciones()
        elif opcion == "6":
            menu_asistencias()
        elif opcion == "7":
            menu_reportes()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

menu()