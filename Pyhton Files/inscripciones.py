
from conexionSQL import get_connection
from validacion_datos import pedir_texto_obligatorio
from validacion_datos import pedir_entero
from estudiantes import listar_estudiantes
from actividades import listar_actividades

def inscribir_estudiante():
    print("\n--- Insribir estudiante ---")

    listar_estudiantes()
    id_estudiante = pedir_entero("Ingrese el ID del Estudiante: ")

    listar_actividades()
    id_actividad_deportiva = pedir_entero("Ingrese el ID de la Actvividad Deportiva: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        estado = "" #tengo que verifcar que la act. este abierta y que tenga cupos disponibles.
        #consulta sql:
        sql_verificar = """
                SELECT estado, cupoMax,
                       (SELECT COUNT(*) FROM inscripciones 
                        WHERE id_actividad_deportiva = %s AND estado = 'confirmada') as inscriptos
                FROM actividadesDeportivas
                WHERE id_actividad = %s
            """
        cursor.execute(sql_verificar, (id_actividad_deportiva, id_actividad_deportiva))
        actividad = cursor.fetchone()

        if actividad is None:
            print("La actividad no existe.")
            return

        if actividad[0] != 'abierta':
            print("La actividad no está abierta.")
            return

        estado = 'confirmada' if actividad[2] < actividad[1] else 'lista_espera'


        sql = """
                INSERT INTO inscripciones 
                (id_estudiante, id_actividad_deportiva, estado)
                VALUES (%s, %s, %s);
            """

        valores = (id_estudiante, id_actividad_deportiva, estado)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Inscricpión creada correctamente.")

    except Exception as e:
        print("Error al crear inscricpción:")
        print(e)
        print("Puede ser que el id del estudiante o  id de la activividad no sea válidos.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()