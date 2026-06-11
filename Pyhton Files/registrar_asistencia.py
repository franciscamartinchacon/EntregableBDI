from conexionSQL import get_connection
from validacion_datos import pedir_texto_obligatorio
from validacion_datos import pedir_entero
from validacion_datos import pedir_bool
from estudiantes import listar_estudiantes
from actividades import listar_actividades
from inscripciones import listar_inscripciones

def registrar_asistencia():
    print("\n--- Registrar asistencia ---")

    listar_inscripciones()
    id_inscripcion = pedir_entero("Ingrese el id de la inscripción: ")

    fecha = #depende si se pide o si es la actual

    presente = pedir_bool("Ingrese s/n para indicar asistencia (s = si | n = no: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
                INSERT INTO asistencias 
                (id_inscripcion, fecha?, presente)
                VALUES (%s, %s, %s);
            """

        valores = (id_inscripcion, fecha?, presente)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Asistencia cargada correctamente.")

    except Exception as e:
        print("Error al cargar asistencia:")
        print(e)
        print("Puede ser que algun id sea inválido.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()




