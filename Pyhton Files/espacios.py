from conexionSQL import get_connection
from validacion_datos import pedir_texto_obligatorio
from validacion_datos import pedir_entero
from validacion_datos import pedir_bool
from main import menu

#Depliega otro menu [agregar, borrar, modificar, disciplinas]

def menu_espacios():
    while True:
        print("\n--- ABM disciplinas ---")
        print("1. Alta espacio deportivo") #Agregar disciplina
        print("2. Borrar espacio deportivo")
        print("3. Actualizar espacio deportivo")
        print("4. Listar espacios deportivo")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            alta_espacio()
        elif opcion == "2":
            borrar_espacio()
        elif opcion == "3":
            actualizar_espacio()
        elif opcion == "4":
            listar_espacios()
        elif opcion == "0":
            print("Saliendo...")
            menu()
            break
        else:
            print("Opción no válida")



def alta_espacio():
    print("\n--- Alta de espacios deportivos ---")

    nombre = pedir_texto_obligatorio("Nombre: ")
    ubicacion = pedir_texto_obligatorio("Ubicación: ")
    libre = pedir_bool("Libre (s/n): ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
               INSERT INTO disciplinas 
               (nombre, ubicacion, libre)
               VALUES (%s,%s,%s);
           """

        valores = (nombre,ubicacion, libre)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Espacio creado correctamente.")

    except Exception as e: #muestra el error específico?
        print("Error al crear espacio:")
        print(e)
        print("Puede ser que el nombre ya exista, o que un tipo de dato sea incorrecto.")

    finally:
        if cursor is not None: #evita el error si algo falló al abrirse al abrir el cursor.
            cursor.close()
        if conexion is not None:
            conexion.close()


def borrar_espacio():
    print("\n--- Eliminar espacio deportivo ---")

    listar_espacios()

    id_espacio = pedir_entero("\nIngrese el ID del espacio a eliminar: ")

    confirmacion = input("¿Seguro que desea eliminar este espacio? (s/n): ").lower()

    if confirmacion != "s":
        print("Operación cancelada.")
        return

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
                DELETE FROM espaciosDeportivos
                WHERE id_espacio = %s;
            """

        cursor.execute(sql, (id_espacio,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Espacio deportivo eliminado correctamente.")
        else:
            print("No se encontró un espacio deportivo con ese ID.")

    except Exception as e:
        print("Error al eliminar espacio deportivo:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def actualizar_espacio():
    """
    Primero muestra la lista de espacios para que el usuario pueda ver el ID.
    Luego pide los nuevos datos y ejecuta un UPDATE.
    """
    print("\n--- Actulizar espacio deportivo ---")

    listar_espacios()

    id_espacio = pedir_entero("\nIngrese el ID del espacio deportivo a modificar: ")

    print("\nIngrese los nuevos datos del espacio: ")
    nombre = pedir_texto_obligatorio("Nuevo nombre: ")
    ubicacion = pedir_texto_obligatorio("Nueva ubicación: ")
    libre = pedir_bool("Libre (s/n): ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
                    UPDATE espaciosDeportivos
                    SET nombre = %s,
                        ubicacion = %s,
                        libre = %s
                    WHERE id_espacio = %s;
                """

        valores = (
            nombre,
            ubicacion,
            libre,
            id_espacio
        )

        cursor.execute(sql, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print("Espacio deportivo modificado correctamente.")
        else:
            print("No se encontró un espacio deportivo con ese ID.")

    except Exception as e:
        print("Error al modificar espacio deportivo:")
        print(e)
        print("Puede ser que el nombre ya exista. O algun tipo de dato esté mal")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def listar_espacios():
    print("\n--- Listado de espacios deportivos ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
                SELECT 
                    e.id_espacio, e.nombre
                FROM espaciosDeportivos e
                ORDER BY e.id_espacio, e.nombre;
            """

        cursor.execute(sql)
        encontro = False
        for espacio in cursor:
            encontro = False
            print(f"ID: {espacio[0]} | Nombre: {espacio[1]}")

        if not encontro:
            print("No hay espacios deportivos cargados")


    except Exception as e:
        print("Error al listar espacios deportivos:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()