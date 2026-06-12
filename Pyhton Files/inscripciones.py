
from conexionSQL import get_connection
from validacion_datos import pedir_entero
from estudiantes import listar_estudiantes
from actividades import listar_actividades, presione_enter

def gestion_inscripciones():
    while True:
        print("\n--- Gestión Inscripciones ---")
        print("1. Inscribir estudiante")
        print("2. Listar inscripciones")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            inscribir_estudiante()
        elif opcion == "2":
            listar_inscripciones()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

def tiene_conflicto_horario(documento, id_actividad_nueva):
    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT COUNT(*)
            FROM inscripciones i
            JOIN actividadesDeportivas actual
                ON i.id_actividad_deportiva = actual.id_actividad
            JOIN actividadesDeportivas nueva
                ON nueva.id_actividad = %s
            WHERE i.documento = %s
              AND i.estado = 'confirmada'
              AND actual.fecha = nueva.fecha
              AND actual.hora_inicio < nueva.hora_fin
              AND actual.hora_fin > nueva.hora_inicio;
        """

        cursor.execute(sql, (id_actividad_nueva, documento))
        resultado = cursor.fetchone()

        return resultado[0] > 0

    except Exception as e:
        print("Error al verificar conflicto de horario:")
        print(e)
        return True

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

# Inscribir estudiante a una actividad
def inscribir_estudiante():
    print("\n--- Insribir estudiante ---")

    listar_estudiantes()
    documento = pedir_entero("Ingrese el documento del Estudiante: ")

    listar_actividades()
    id_actividad = pedir_entero("Ingrese el ID de la Actvividad Deportiva: ")

    if tiene_conflicto_horario(documento, id_actividad):
        print("El estudiante ya tiene una actividad confirmada en ese horario.")
        return

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        # para fijar el estado tengo que verifcar que la act. este abierta y que tenga cupos disponibles.
        #consulta sql: revisa cant de inscptos acutalmente con el id de la act.
        sql_verificar = """
                SELECT estado, cupoMax,
                       (SELECT COUNT(*) FROM inscripciones 
                        WHERE id_actividad = %s AND estado = 'confirmada') as inscriptos
                FROM actividadesDeportivas
                WHERE id_actividad = %s
            """

        cursor.execute(sql_verificar, (id_actividad, id_actividad))
        actividad = cursor.fetchone()

        if actividad is None:
            print("La actividad no existe.")
            return

        if actividad[0] != 'abierta': #actividad [0] = estado (orden del select)
            print("La actividad no está abierta, por ende no se puede realizar la inscripción. ")
            return

        estado = 'confirmada' if actividad[2] < actividad[1] else 'lista_espera' #actividad[2] = inscriptos, y [1] cupo max


        sql = """
                INSERT INTO inscripciones 
                (documento, id_actividad, estado)
                VALUES (%s, %s, %s);
            """

        valores = (documento, id_actividad, estado)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Inscricpión creada correctamente.")

    except Exception as e:
        print("Error al crear inscricpción:")
        print(e)
        print("Puede ser que el documento del estudiante o  id de la activividad no sea válidos.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
        presione_enter()


def listar_inscripciones():
    print("\n--- Listado de inscripciones ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
                    SELECT 
                        i.id_inscripcion, i.documento, i.id_actividad, i.fecha_inscripcion, i.estado
                    FROM inscripciones i
                    ORDER BY  i.id_inscripcion;
                """

        cursor.execute(sql)
        encontro = False
        for inscripcion in cursor:
            encontro = False
            print(f"ID Inscripción: {inscripcion[0]} | Documento Estudiante: {inscripcion[1]} | ID Actividad Deportiva: {inscripcion[2]} | Fecha: {inscripcion[3]} | Estado: {inscripcion[4]}")

        if not encontro:
            print("No hay inscripciones cargadas")


    except Exception as e:
        print("Error al listar inscripciones:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()
        presione_enter()