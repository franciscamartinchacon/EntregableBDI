from conexionSQL import get_connection
from validacion_datos import pedir_texto_obligatorio
from validacion_datos import pedir_entero

#Depliega otro menu [agregar, borrar, modificar, disciplinas]

def menu_disciplinas():
    while True:
        print("\n--- ABM disciplinas ---")
        print("1. Alta disciplina") #Agregar disciplina
        print("2. Borrar disciplina")
        print("3. Actualizar disciplina")
        print("4. Listar disciplinas")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            alta_disciplina()
        elif opcion == "2":
            borrar_disciplina()
        elif opcion == "3":
            actualizar_disciplina()
        elif opcion == "4":
            listar_disciplinas()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")



def alta_disciplina():
    print("\n--- Alta de disciplinas ---")

    nombre = pedir_texto_obligatorio("Nombre: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
               INSERT INTO disciplinas 
               (nombre)
               VALUES (%s);
           """

        valores = (nombre,)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Disciplina creada correctamente.")

    except Exception as e: #muestra el error específico?
        print("Error al crear disciplina:")
        print(e)
        print("Puede ser que el nombre ya existan.")

    finally:
        if cursor is not None:#evita el error si algo falló al abrirse al abrir el cursor.
            cursor.close()
        if conexion is not None:
            conexion.close()


def borrar_disciplina():
    print("\n--- Eliminar disciplina ---")

    listar_disciplinas()

    id_disciplina = pedir_entero("\nIngrese el ID de la disciplina a eliminar: ")

    confirmacion = input("¿Seguro que desea eliminar esta disciplina? (si/no): ").lower()

    if confirmacion != "s":
        print("Operación cancelada.")
        return

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
                DELETE FROM disciplinas
                WHERE id_disciplina = %s;
            """

        cursor.execute(sql, (id_disciplina,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Disciplina eliminada correctamente.")
        else:
            print("No se encontró una disciplina con ese ID.")

    except Exception as e:
        print("Error al eliminar disciplina, puede que haya una actividad relacionada:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def actualizar_disciplina():
    """
    Primero muestra la lista de disciplinas para que el usuario pueda ver el ID.
    Luego pide los nuevos datos y ejecuta un UPDATE.
    """
    print("\n--- Actulizar disciplina ---")

    listar_disciplinas()

    id_disciplina = pedir_entero("\nIngrese el ID de la disciplina a modificar: ")

    print("\nIngrese los nuevos datos de la disciplina:")
    nombre = pedir_texto_obligatorio("Nuevo nombre: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE disciplinas
            SET nombre = %s,
            WHERE id_disciplina = %s;
        """

        valores = (
            nombre,
            id_disciplina
        )

        cursor.execute(sql, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print("Disciplina modificada correctamente.")
        else:
            print("No se encontró una disciplina con ese ID.")

    except Exception as e:
        print("Error al modificar disciplina:")
        print(e)
        print("Puede ser que el nombre ya exista.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def listar_disciplinas():
    print("\n--- Listado de disciplinas ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
                SELECT 
                    d.id_disciplina, d.nombre
                FROM disciplinas d
                ORDER BY d.id_disciplina, d.nombre;
            """

        cursor.execute(sql)
        disciplinas = cursor.fetchall()

        if len(disciplinas) == 0:
            print("No hay disciplinas cargadas")
        else:
            for disciplina in disciplinas:
                print(f"ID: {disciplina[0]} | Nombre: {disciplina[1]}")

    except Exception as e:
        print("Error al listar disciplinas")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()