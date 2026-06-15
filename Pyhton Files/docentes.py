from conexionSQL import get_connection
from validacion_datos import pedir_texto_obligatorio, pedir_bool, pedir_cedula, presione_enter

def menu_docentes():
    while True:
        print("\n--- ABM Docentes ---")
        print("1. Alta docente")
        print("2. Listar docente")
        print("3. Modificar docente")
        print("4. Eliminar docente")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            alta_docente()
            presione_enter()
        elif opcion == "2":
            listar_docentes()
            presione_enter()
        elif opcion == "3":
            modificar_docente()
            presione_enter()
        elif opcion == "4":
            eliminar_docente()
            presione_enter()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


# ALTA DOCENTE

def alta_docente():

    print("\n--- Alta de docente ---")

    documento = pedir_cedula("Documento: ")
    nombre = pedir_texto_obligatorio("Nombre: ")
    apellido = pedir_texto_obligatorio("Apellido: ")
    correo = pedir_texto_obligatorio("Correo electrónico: ")
    contrasena = pedir_texto_obligatorio("Contraseña: ") #solo para ingresar

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO docentes 
            (documento, nombre, apellido, correo, contrasena)
            VALUES (%s, %s, %s, %s, %s);
        """

        valores = (documento, nombre, apellido, correo,contrasena)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Docente creado correctamente.")

    except Exception as e:
        print("Error al crear docente:")
        print(e)
        print("Puede ser que el documento o el correo ya existan.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def listar_docentes():

    print("\n--- Listado de docentes ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT 
                d.documento,
                d.nombre,
                d.apellido,
                d.correo
            FROM docentes d
            ORDER BY d.documento, d.apellido, d.nombre;
        """

        cursor.execute(sql)
        docentes = cursor.fetchall()

        if len(docentes) == 0:
            print("No hay docentes registrados.")
        else:
            for docente in docentes:
                print(
                    f"Documento: {docente[0]} | "
                    f"Nombre: {docente[1]} | "
                    f"Apellido: {docente[2]} | "
                    f"Correo: {docente[3]} | "
                )

    except Exception as e:
        print("Error al listar docentes:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def modificar_docente():

    print("\n--- Modificar docente ---")

    listar_docentes()

    documento = pedir_cedula("\nIngrese el documento del docente a modificar: ")

    while True:
        print("\n--- Ingrese el dato que quiere modificar ---")
        print("1. Nombre del docente")
        print("2. Apellido del docente")
        print("3. Correo del docente")
        print("0. Volver al menú de docente")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            modificar_nombre(documento)
        elif opcion == "2":
            modificar_apellido(documento)
        elif opcion == "3":
            modificar_correo(documento)

        elif opcion == "0":
            print("Volviendo al menú de docentes...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

def modificar_nombre(documento):
    print("\nIngrese el nuevo nombre del docente")

    nombre = pedir_texto_obligatorio("Nuevo nombre: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE docentes
            SET nombre = %s
            WHERE documento = %s;
        """

        valores = (nombre, documento)

        cursor.execute(sql, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print("Nombre modificado correctamente.")
        else:
            print("No se encontró un docente con ese documento.")

    except Exception as e:
        print("Error al modificar el nombre del docente:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def modificar_apellido(documento):
    print("\nIngrese el nuevo apellido del docente")
    apellido = pedir_texto_obligatorio("Nuevo apellido: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE docentes
            SET apellido = %s
            WHERE documento = %s;
        """

        cursor.execute(sql, (apellido, documento))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Apellido modificado correctamente.")
        else:
            print("No se encontró un docente con ese documento.")

    except Exception as e:
        print("Error al modificar el apellido:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def modificar_correo(documento):
    print("\nIngrese el nuevo correo del docente")
    correo = pedir_texto_obligatorio("Nuevo correo: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE docentes
            SET correo = %s
            WHERE documento = %s;
        """

        cursor.execute(sql, (correo, documento))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Correo modificado correctamente.")
        else:
            print("No se encontró un docente con ese documento.")

    except Exception as e:
        print("Error al modificar el correo:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def eliminar_docente():
    print("\n--- Eliminar docente ---")

    listar_docentes()

    documento = pedir_cedula("\nIngrese el documento del docente a eliminar: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        #Verificar si el docente existe
        sql_existe = """
            SELECT COUNT(*)
            FROM docentes
            WHERE documento = %s;
        """

        cursor.execute(sql_existe, (documento,))
        existe = cursor.fetchone()[0]

        if existe == 0:
            print("No existe un docente con ese documento.")
            return

        #Verificar si dicta alguna activdad
        sql_actividades = """
            SELECT COUNT(*)
            FROM actividadesDeportivas
            WHERE docente_asignado = %s;
        """

        cursor.execute(sql_actividades, (documento,))
        cantidad_actividades = cursor.fetchone()[0]

        if cantidad_actividades > 0:
            print(f"El docente tiene {cantidad_actividades} actividad/es asignada/s.")

            respuesta = pedir_bool("¿Querés reasignar esas actividades a otro docente? (si/no): ")

            if respuesta == False:
                print("No se eliminó el docente.")
                return

            print("\nSeleccione el nuevo docente para esas actividades:")
            listar_docentes()

            nuevo_docente = pedir_cedula("Ingrese el documento del nuevo docente: ")

            if nuevo_docente == documento:
                print("No podés reasignar las actividades al mismo docente que querés eliminar.")
                return

            # Verificar que el nuevo docente exista
            sql_nuevo_docente = """
                        SELECT COUNT(*)
                        FROM docentes
                        WHERE documento = %s;
                    """

            cursor.execute(sql_nuevo_docente, (nuevo_docente,))
            existe_nuevo_docente = cursor.fetchone()[0]

            if existe_nuevo_docente == 0:
                print("No existe un docente con ese documento.")
                return

            # Reasignar actividades
            sql_reasignar = """
                        UPDATE actividadesDeportivas
                        SET docente_asignado = %s
                        WHERE docente_asignado = %s;
                    """

            cursor.execute(sql_reasignar, (nuevo_docente, documento))

            print("Actividades reasignadas correctamente.")

        confirmacion = input("¿Seguro que desea eliminar este docente? (si/no): ").strip().lower()

        if confirmacion not in ["s", "si"]:
            print("Operación cancelada.")
            conexion.rollback()
            return

        # Borrar docente
        sql_borrar_docente = """
                    DELETE FROM docentes
                    WHERE documento = %s;
                """

        cursor.execute(sql_borrar_docente, (documento,))
        conexion.commit()

        print("Docente eliminado correctamente.")

    except Exception as e:
        if conexion is not None:
            conexion.rollback()

        print("Error al eliminar docente.")
        print("No se guardaron los cambios realizados.")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()