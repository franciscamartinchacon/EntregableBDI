from conexionSQL import get_connection

# Funciones para validar

def pedir_texto_obligatorio(mensaje):
    # Pide un texto por consola y valida que no esté vacío.
    while True:
        valor = input(mensaje).strip()

        if valor != "":
            return valor

        print("Error. Este campo no puede estar vacío.")


def pedir_entero(mensaje):

    while True:
        valor = input(mensaje).strip()

        if valor.isdigit():
            return int(valor)

        print("Error: debe ingresar un número válido.")


# MENÚ DE ESTUDIANTES

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
        elif opcion == "2":
            listar_estudiantes()
        elif opcion == "3":
            modificar_estudiante()
        elif opcion == "4":
            eliminar_estudiante()
        elif opcion == "0":
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


# ALTA DE ESTUDIANTE

def alta_estudiante():

    print("\n--- Alta de estudiante ---")

    documento = pedir_texto_obligatorio("Documento: ")
    nombre = pedir_texto_obligatorio("Nombre: ")
    apellido = pedir_texto_obligatorio("Apellido: ")
    correo = pedir_texto_obligatorio("Correo electrónico: ")

    listar_carreras()
    id_carrera = pedir_entero("Ingrese el ID de la carrera: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO estudiantes 
            (documento, nombre, apellido, correo, id_carrera)
            VALUES (%s, %s, %s, %s, %s);
        """

        valores = (documento, nombre, apellido, correo, id_carrera)

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


# LISTAR ESTUDIANTES

def listar_estudiantes():

    print("\n--- Listado de estudiantes ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT 
                e.id_estudiante,
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
            ORDER BY e.apellido, e.nombre;
        """

        cursor.execute(sql)
        estudiantes = cursor.fetchall()

        if len(estudiantes) == 0:
            print("No hay estudiantes registrados.")
        else:
            for estudiante in estudiantes:
                print(
                    f"ID: {estudiante[0]} | "
                    f"Documento: {estudiante[1]} | "
                    f"Nombre: {estudiante[2]} {estudiante[3]} | "
                    f"Correo: {estudiante[4]} | "
                    f"Carrera: {estudiante[5]} | "
                    f"Facultad: {estudiante[6]}"
                )

    except Exception as e:
        print("Error al listar estudiantes:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


# ============================================================
# MODIFICAR ESTUDIANTE
# ============================================================

def modificar_estudiante():
    """
    Modifica los datos de un estudiante existente.

    Primero muestra la lista de estudiantes para que el usuario pueda ver el ID.
    Luego pide los nuevos datos y ejecuta un UPDATE.
    """
    print("\n--- Modificar estudiante ---")

    listar_estudiantes()

    id_estudiante = pedir_entero("\nIngrese el ID del estudiante a modificar: ")

    print("\nIngrese los nuevos datos del estudiante:")
    documento = pedir_texto_obligatorio("Nuevo documento: ")
    nombre = pedir_texto_obligatorio("Nuevo nombre: ")
    apellido = pedir_texto_obligatorio("Nuevo apellido: ")
    correo = pedir_texto_obligatorio("Nuevo correo electrónico: ")

    listar_carreras()
    id_carrera = pedir_entero("Nuevo ID de carrera: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE estudiantes
            SET documento = %s,
                nombre = %s,
                apellido = %s,
                correo = %s,
                id_carrera = %s
            WHERE id_estudiante = %s;
        """

        valores = (
            documento,
            nombre,
            apellido,
            correo,
            id_carrera,
            id_estudiante
        )

        cursor.execute(sql, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print("Estudiante modificado correctamente.")
        else:
            print("No se encontró un estudiante con ese ID.")

    except Exception as e:
        print("Error al modificar estudiante:")
        print(e)
        print("Puede ser que el documento o correo ya existan, o que la carrera no sea válida.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


# ============================================================
# ELIMINAR ESTUDIANTE
# ============================================================

def eliminar_estudiante():
    """
    Elimina un estudiante de la base de datos.

    Importante:
    Si el estudiante tiene inscripciones asociadas, MySQL puede impedir
    la eliminación por la clave foránea. En ese caso, se muestra un mensaje.
    """
    print("\n--- Eliminar estudiante ---")

    listar_estudiantes()

    id_estudiante = pedir_entero("\nIngrese el ID del estudiante a eliminar: ")

    confirmacion = input("¿Seguro que desea eliminar este estudiante? (s/n): ").lower()

    if confirmacion != "s":
        print("Operación cancelada.")
        return

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            DELETE FROM estudiantes
            WHERE id_estudiante = %s;
        """

        cursor.execute(sql, (id_estudiante,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Estudiante eliminado correctamente.")
        else:
            print("No se encontró un estudiante con ese ID.")

    except Exception as e:
        print("Error al eliminar estudiante:")
        print(e)
        print("No se puede eliminar si el estudiante tiene inscripciones asociadas.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
