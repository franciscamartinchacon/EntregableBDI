from conexionSQL import get_connection
from validacion_datos import pedir_entero, pedir_texto_obligatorio, presione_enter
from estudiantes import menu_estudiantes
from docentes import menu_docentes
from actividades import menu_actividades, listar_actividades
from inscripciones import gestion_inscripciones, inscribirme_a_actividad, ver_mis_inscripciones
from asistencias import menu_asistencias
from reportes import menu_reportes

def login():
    while True:
        print("\n -- Inicio de sesión -- ")
        print("1. Iniciar sesión")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            iniciar_sesion()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")


def iniciar_sesion():
    print("\n -- Para iniciar sesión, ingrese:  -- ")

    documento = pedir_entero("Documento: ")
    contrasena = input("Contraseña: ") #no requiere ninguna caracteristica especial

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        #Consulta en SQL para determinar el rol del usuario.
        #Busca el docuemnto y la contra en todas las tablas
        busca_usuario = True

        #busca en admins primero
        while busca_usuario == True:
            sql_admin = """
                    SELECT documento, nombre, apellido
                    FROM admins
                    WHERE documento = %s
                    AND contrasena = %s
                """

            cursor.execute(sql_admin, (documento, contrasena))
            admin = cursor.fetchone() #sin impirimir, solo lo guarda en admin

            if admin is not None:
                print(f"\nBienvenido/a Admin: {admin[1]} {admin[2]}")
                menu_admins()
                return #deja de buscar


            #busca en docentes
            sql_docentes = """
                    SELECT documento, nombre, apellido
                    FROM docentes
                    WHERE documento = %s
                    AND contrasena = %s
                            """

            cursor.execute(sql_docentes, (documento, contrasena))
            docente = cursor.fetchone()  # sin impirimir, solo lo guarda en admin

            if docente is not None:
                print(f"\nBienvenido/a Docente: {docente[1]} {docente[2]}")
                menu_para_docentes()
                return

            #busca en estudiantes
            sql_estudiante = """
                    SELECT documento, nombre, apellido
                    FROM docentes
                    WHERE documento = %s
                    AND contrasena = %s
                            """

            cursor.execute(sql_estudiante, (documento, contrasena))
            estudiante = cursor.fetchone()  # sin impirimir, solo lo guarda en admin

            if estudiante is not None:
                print(f"\nBienvenido/a Estudiante: {estudiante[1]} {estudiante[2]}")
                menu_para_estudiante()
                return

            #si sigue recorriendo porque no encontró nada
            print("Documento o contraseña incorrectos.")

    except Exception as e:
        print("Error al iniciar sesión:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def menu_admins():
    while True:
        print("\n--- Menú Admin ---")
        print("1. Gestionar estudiantes")
        print("2. Gestionar docentes")
        print("3. Gestionar actividades deportivas")
        print("4. Gestionar inscripciones")
        print("5. Gestionar asistencias")
        print("6. Ver reportes")
        print("0. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_estudiantes()
            presione_enter()
        elif opcion == "2":
            menu_docentes()
            presione_enter()
        elif opcion == "3":
            menu_actividades()
            presione_enter()
        elif opcion == "4":
            gestion_inscripciones()
            presione_enter()
        elif opcion == "5":
            menu_asistencias()
            presione_enter()
        elif opcion == "6":
            menu_reportes()
            presione_enter()
        elif opcion == "0":
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida.")

def menu_para_docentes():
    while True:
        print("\n--- Menú Docente ---")
        print("1. Ver actividades deportivas")
        print("2. Registrar asistencias")
        print("3. Ver reportes")
        print("0. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listar_actividades()
            presione_enter()
        elif opcion == "2":
            menu_asistencias()
            presione_enter()
        elif opcion == "3":
            menu_reportes()
            presione_enter()
        elif opcion == "0":
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida.")

def menu_para_estudiante(documento):
    while True:
        print("\n--- Menú Estudiante ---")
        print("1. Ver actividades deportivas")
        print("2. Inscribirme a una actividad")
        print("3. Ver mis inscripciones")
        print("0. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listar_actividades()
            presione_enter()
        elif opcion == "2":
            inscribirme_a_actividad(documento)
            presione_enter()
        elif opcion == "3":
            ver_mis_inscripciones(documento)
            presione_enter()
        elif opcion == "0":
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida.")
