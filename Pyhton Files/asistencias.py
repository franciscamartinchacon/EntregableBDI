from conexionSQL import get_connection
from validacion_datos import pedir_entero, pedir_texto_obligatorio, pedir_opcion_valida,presione_enter

def menu_asistencias():

    while True:
        print("\n--- Registro de Asistencias ---")
        print("1. Registrar asistencia")
        print("2. Listar asistencias")
        print("3. Listar inscripciones confirmadas")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_asistencia()
            presione_enter()
        elif opcion == "2":
            listar_asistencias()
            presione_enter()
        elif opcion == "3":
            listar_inscripciones_confirmadas()
            presione_enter()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

def listar_inscripciones_confirmadas():

    print("\n--- Inscripciones confirmadas ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT i.id_inscripcion, e.documento, e.nombre, e.apellido, a.nombre AS actividad, i.estado
            FROM inscripciones i
            JOIN estudiantes e ON i.documento = e.documento
            JOIN actividadesDeportivas a ON i.id_actividad_deportiva = a.id_actividad
            WHERE i.estado = 'confirmada'
            ORDER BY a.nombre, e.apellido, e.nombre;
        """

        cursor.execute(sql)
        inscripciones = cursor.fetchall()

        if len(inscripciones) == 0:
            print("No hay inscripciones confirmadas.")
        else:
            for inscripcion in inscripciones:
                print(
                    f"ID inscripción: {inscripcion[0]} | "
                    f"Documento: {inscripcion[1]} | "
                    f"Estudiante: {inscripcion[2]} {inscripcion[3]} | "
                    f"Actividad: {inscripcion[4]} | "
                    f"Estado: {inscripcion[5]}"
                )

    except Exception as e:
        print("Error al listar inscripciones confirmadas.")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
    

def obtener_inscripcion_confirmada(id_inscripcion):

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT i.id_inscripcion, i.estado, e.nombre, e.apellido, a.nombre AS actividad
            FROM inscripciones i
            JOIN estudiantes e ON i.documento = e.documento
            JOIN actividadesDeportivas a ON i.id_actividad_deportiva = a.id_actividad
            WHERE i.id_inscripcion = %s;
        """

        cursor.execute(sql, (id_inscripcion,))
        inscripcion = cursor.fetchone()

        if inscripcion is None:
            return None

        if inscripcion[1] != "confirmada":
            return None

        return inscripcion

    except Exception as e:
        print("Error al validar la inscripción.")
        print(e)
        return None

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def registrar_asistencia():

    print("\n--- Registrar asistencia ---")

    listar_inscripciones_confirmadas()

    id_inscripcion = pedir_entero("\nIngrese el ID de la inscripción: ")

    inscripcion = obtener_inscripcion_confirmada(id_inscripcion)

    if inscripcion is None:
        print("No se puede registrar asistencia.")
        print("La inscripción no existe o no está confirmada.")
        return

    print(
        f"\nInscripción seleccionada: "
        f"{inscripcion[2]} {inscripcion[3]} | Actividad: {inscripcion[4]}"
    )

    fecha_sql = pedir_texto_obligatorio("Fecha de asistencia (AAAA-MM-DD): ")

    opciones_validas = ["si", "no"]
    respuesta = pedir_opcion_valida("¿Estuvo presente? (si/no): ", opciones_validas)

    if respuesta == "si":
        presente = True
    else:
        presente = False

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO asistencias
            (id_inscripcion, fecha, presente)
            VALUES (%s, %s, %s);
        """

        valores = (id_inscripcion, fecha_sql, presente)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Asistencia registrada correctamente.")

    except Exception as e:
        print("Error al registrar asistencia.")
        print(e)
        print("Revise que la fecha tenga formato AAAA-MM-DD.")
        print("También puede ser que ya exista una asistencia registrada para esa inscripción en esa fecha.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def listar_asistencias():

    print("\n--- Listado de asistencias ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT asis.id_asistencia, asis.fecha, asis.presente, e.documento, e.nombre, e.apellido, a.nombre AS actividad
            FROM asistencias asis
            JOIN inscripciones i ON asis.id_inscripcion = i.id_inscripcion
            JOIN estudiantes e ON i.documento = e.documento
            JOIN actividadesDeportivas a ON i.id_actividad_deportiva = a.id_actividad
            ORDER BY asis.fecha, a.nombre, e.apellido, e.nombre;
        """

        cursor.execute(sql)
        asistencias = cursor.fetchall()

        if len(asistencias) == 0:
            print("No hay asistencias registradas.")
        else:
            for asistencia in asistencias:
                if asistencia[2] == 1:
                    estado_asistencia = "Presente"
                else:
                    estado_asistencia = "Ausente"

                print(
                    f"ID asistencia: {asistencia[0]} | "
                    f"Fecha: {asistencia[1]} | "
                    f"Documento: {asistencia[3]} | "
                    f"Estudiante: {asistencia[4]} {asistencia[5]} | "
                    f"Actividad: {asistencia[6]} | "
                    f"Asistencia: {estado_asistencia}"
                )

    except Exception as e:
        print("Error al listar asistencias.")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()