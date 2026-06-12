from conexionSQL import get_connection
from validacion_datos import pedir_texto_obligatorio
from validacion_datos import pedir_entero
from validacion_datos import pedir_bool, presione_enter


def menu_espacios():
    while True:
        print("\n--- ABM espacios deportivos ---")
        print("1. Alta de espacio deportivo") #Agregar disciplina
        print("2. Borrar espacio deportivo")
        print("3. Modificar espacio deportivo")
        print("4. Listar espacios deportivos")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            alta_espacio()
            presione_enter()
        elif opcion == "2":
            borrar_espacio()
            presione_enter()
        elif opcion == "3":
            modificar_espacio()
            presione_enter()
        elif opcion == "4":
            listar_espacios()
            presione_enter()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")


def alta_espacio():
    print("\n--- Alta de espacios deportivos ---")

    nombre = pedir_texto_obligatorio("Nombre: ")
    ubicacion = pedir_texto_obligatorio("Ubicación: ")
    libre = pedir_bool("Libre (si/no): ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO espaciosDeportivos
            (nombre, ubicacion, libre)
            VALUES (%s, %s, %s);
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

    confirmacion = input("¿Seguro que desea eliminar este espacio? (si/no): ").lower()

    if confirmacion != "si":
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


def modificar_espacio():

    print("\n--- Modificar espacio deportivo ---")

    listar_espacios()

    id_espacio = pedir_entero("\nIngrese el ID del espacio deportivo a modificar: ")

    while True:
        print("\n--- Ingrese el dato que quiere modificar ---")
        print("1. Nombre del espacio")
        print("2. Ubicación del espacio")
        print("3. Estado libre/ocupado")
        print("0. Volver al menú de espacios")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            modificar_nombre_espacio(id_espacio)
        elif opcion == "2":
            modificar_ubicacion_espacio(id_espacio)
        elif opcion == "3":
            modificar_libre_espacio(id_espacio)
        elif opcion == "0":
            print("Volviendo al menú de espacios...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

def modificar_nombre_espacio(id_espacio):

    nombre = pedir_texto_obligatorio("Nuevo nombre: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE espaciosDeportivos
            SET nombre = %s
            WHERE id_espacio = %s;
        """

        cursor.execute(sql, (nombre, id_espacio))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Nombre del espacio modificado correctamente.")
        else:
            print("No se encontró un espacio deportivo con ese ID.")

    except Exception as e:
        print("Error al modificar el nombre del espacio:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def modificar_ubicacion_espacio(id_espacio):

    ubicacion = pedir_texto_obligatorio("Nueva ubicación: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE espaciosDeportivos
            SET ubicacion = %s
            WHERE id_espacio = %s;
        """

        cursor.execute(sql, (ubicacion, id_espacio))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Ubicación del espacio modificada correctamente.")
        else:
            print("No se encontró un espacio deportivo con ese ID.")

    except Exception as e:
        print("Error al modificar la ubicación del espacio:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def modificar_libre_espacio(id_espacio):

    libre = pedir_bool("Libre (si/no): ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE espaciosDeportivos
            SET libre = %s
            WHERE id_espacio = %s;
        """

        cursor.execute(sql, (libre, id_espacio))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Estado del espacio modificado correctamente.")
        else:
            print("No se encontró un espacio deportivo con ese ID.")

    except Exception as e:
        print("Error al modificar el estado del espacio:")
        print(e)

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
                SELECT e.id_espacio, e.nombre, e.ubicacion, e.libre
                FROM espaciosDeportivos e
                ORDER BY e.id_espacio, e.nombre;
            """

        cursor.execute(sql)
        espacios = cursor.fetchall()

        if len(espacios) == 0:
            print("No hay espacios deportivos cargados")
        else:
            for espacio in espacios:
                if espacio[3] == 1:
                    estado_libre = "Sí"
                else:
                    estado_libre = "No"

                print(f"ID: {espacio[0]} | "f"Nombre: {espacio[1]} | "f"Ubicación: {espacio[2]} | "f"Libre: {estado_libre}")


    except Exception as e:
        print("Error al listar espacios deportivos:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()