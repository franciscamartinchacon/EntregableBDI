from conexionSQL import get_connection
from validacion_datos import pedir_texto_obligatorio, pedir_entero, pedir_cedula, presione_enter

def menu_estudiantes():
    while True:
        print("\n--- ABM Estudiantes ---")
        print("1. Alta estudiante")
        print("2. Listar estudiantes")
        print("3. Modificar estudiante")
        print("4. Eliminar estudiante")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            alta_estudiante()
            presione_enter()
        elif opcion == "2":
            listar_estudiantes()
            presione_enter()
        elif opcion == "3":
            modificar_estudiante()
            presione_enter()
        elif opcion == "4":
            eliminar_estudiante()
            presione_enter()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


# LISTAR CARRERAS

def listar_carreras():
    #Lista las carreras disponibles junto con su facultad.
    #En la tabla estudiantes no se guarda el texto de la carrera, sino el id_carrera.

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT 
                c.id_carrera,
                c.nombre AS carrera,
                f.nombre AS facultad
            FROM carreras c
            JOIN facultades f 
                ON c.id_facultad = f.id_facultad
            ORDER BY f.nombre, c.nombre;
        """

        cursor.execute(sql)
        carreras = cursor.fetchall()

        print("\n--- Carreras disponibles ---")

        if len(carreras) == 0:
            print("No hay carreras registradas.")
        else:
            for carrera in carreras:
                print(f"ID: {carrera[0]} | Carrera: {carrera[1]} | Facultad: {carrera[2]}")

    except Exception as e:
        print("Error al listar carreras:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def alta_estudiante():

    print("\n--- Alta de estudiante ---")

    documento = pedir_cedula("Documento: ")
    nombre = pedir_texto_obligatorio("Nombre: ")
    apellido = pedir_texto_obligatorio("Apellido: ")
    correo = pedir_texto_obligatorio("Correo electrónico: ")
    contrasena = pedir_texto_obligatorio("COntraseña: ") #solo para ingresar

    listar_carreras()
    id_carrera = pedir_entero("Ingrese el ID de la carrera: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO estudiantes 
            (documento, nombre, apellido, correo, contrasena, id_carrera)
            VALUES (%s, %s, %s, %s,%s, %s);
        """

        valores = (documento, nombre, apellido, correo, contrasena, id_carrera)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Estudiante creado correctamente.")

    except Exception as e:
        print("Error al crear estudiante:")
        print(e)
        print("Puede ser que el documento o el correo ya existan, o que la carrera no sea válida.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def listar_estudiantes():

    print("\n--- Listado de estudiantes ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT 
                e.documento,
                e.nombre,
                e.apellido,
                e.correo,
                c.nombre AS carrera,
                f.nombre AS facultad
            FROM estudiantes e
            JOIN carreras c 
                ON e.id_carrera = c.id_carrera
            JOIN facultades f 
                ON c.id_facultad = f.id_facultad
            ORDER BY e.documento, e.apellido, e.nombre;
        """

        cursor.execute(sql)
        estudiantes = cursor.fetchall()

        if len(estudiantes) == 0:
            print("No hay estudiantes registrados.")
        else:
            for estudiante in estudiantes:
                print(
                    f"Documento: {estudiante[0]} | "
                    f"Nombre: {estudiante[1]} | "
                    f"Apellido: {estudiante[2]} | "
                    f"Correo: {estudiante[3]} | "
                    f"Carrera: {estudiante[4]} | "
                    f"Facultad: {estudiante[5]}"
                )

    except Exception as e:
        print("Error al listar estudiantes:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def modificar_estudiante():

    print("\n--- Modificar estudiante ---")

    listar_estudiantes()

    documento = pedir_cedula("\nIngrese el documento del estudiante a modificar: ")

    while True:
        print("\n--- Ingrese el dato que quiere modificar ---")
        print("1. Nombre del estudiante")
        print("2. Apellido del estudiante")
        print("3. Correo del estudiante")
        print("4. Carrera del estudiante")
        print("0. Volver al menú de estudiantes")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            modificar_nombre(documento)
        elif opcion == "2":
            modificar_apellido(documento)
        elif opcion == "3":
            modificar_correo(documento)
        elif opcion == "4":
            modificar_carrera(documento)
        elif opcion == "0":
            print("Volviendo al menú de estudiantes...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

def modificar_nombre(documento):
    print("\nIngrese el nuevo nombre del estudiante:")

    nombre = pedir_texto_obligatorio("Nuevo nombre: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE estudiantes
            SET nombre = %s
            WHERE documento = %s;
        """

        valores = (nombre, documento)

        cursor.execute(sql, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print("Nombre modificado correctamente.")
        else:
            print("No se encontró un estudiante con ese documento.")

    except Exception as e:
        print("Error al modificar el nombre del estudiante:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def modificar_apellido(documento):
    apellido = pedir_texto_obligatorio("Nuevo apellido: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE estudiantes
            SET apellido = %s
            WHERE documento = %s;
        """

        cursor.execute(sql, (apellido, documento))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Apellido modificado correctamente.")
        else:
            print("No se encontró un estudiante con ese documento.")

    except Exception as e:
        print("Error al modificar el apellido:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def modificar_correo(documento):
    correo = pedir_texto_obligatorio("Nuevo correo: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE estudiantes
            SET correo = %s
            WHERE documento = %s;
        """

        cursor.execute(sql, (correo, documento))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Correo modificado correctamente.")
        else:
            print("No se encontró un estudiante con ese documento.")

    except Exception as e:
        print("Error al modificar el correo:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def modificar_carrera(documento):
    print("\n--- Carreras disponibles ---")
    listar_carreras()

    id_carrera = pedir_entero("Ingrese el ID de la nueva carrera: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE estudiantes
            SET id_carrera = %s
            WHERE documento = %s;
        """

        cursor.execute(sql, (id_carrera, documento))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Carrera modificada correctamente.")
        else:
            print("No se encontró un estudiante con ese documento.")

    except Exception as e:
        print("Error al modificar la carrera:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def eliminar_estudiante():
    print("\n--- Eliminar estudiante ---")

    listar_estudiantes()

    documento = pedir_cedula("\nIngrese el documento del estudiante a eliminar: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        #Verificar si el estudiante existe
        sql_existe = """
            SELECT COUNT(*)
            FROM estudiantes
            WHERE documento = %s;
        """

        cursor.execute(sql_existe, (documento,))
        existe = cursor.fetchone()[0]

        if existe == 0:
            print("No existe un estudiante con ese documento.")
            return

        # Verificar si tiene inscripciones
        sql_inscripciones = """
            SELECT COUNT(*)
            FROM inscripciones
            WHERE documento = %s;
        """

        cursor.execute(sql_inscripciones, (documento,))
        cantidad_inscripciones = cursor.fetchone()[0]

        if cantidad_inscripciones > 0:
            print(f"El estudiante tiene {cantidad_inscripciones} inscripción/es asociada/s.")
            respuesta = input("¿Querés borrar también sus inscripciones y asistencias? (si/no): ").strip().lower()

            if respuesta != "si":
                print("No se eliminó el estudiante.")
                return

            #Borrar asistencias asociadas a las inscripciones del estudiante
            sql_borrar_asistencias = """
                DELETE a
                FROM asistencias a
                JOIN inscripciones i
                    ON a.id_inscripcion = i.id_inscripcion
                WHERE i.documento = %s;
            """

            cursor.execute(sql_borrar_asistencias, (documento,))

            #Borrar inscripciones del estudiante
            sql_borrar_inscripciones = """
                DELETE FROM inscripciones
                WHERE documento = %s;
            """

            cursor.execute(sql_borrar_inscripciones, (documento,))

        else:
            confirmacion = input("¿Seguro que desea eliminar este estudiante? (si/no): ").strip().lower()

            if confirmacion != "si":
                print("Operación cancelada.")
                return

        #Borrar estudiante
        sql_borrar_estudiante = """
            DELETE FROM estudiantes
            WHERE documento = %s;
        """

        cursor.execute(sql_borrar_estudiante, (documento,))
        conexion.commit()

        print("Estudiante eliminado correctamente.")

    except Exception as e:
        if conexion is not None:
            conexion.rollback()

        print("Error al eliminar estudiante:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()