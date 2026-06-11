
from conexionSQL import get_connection
from validacion_datos import pedir_entero
from estudiantes import listar_estudiantes
from actividades import listar_actividades
from main import menu

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
            menu()
            break
        else:
            print("Opción inválida. Intente nuevamente.")

# Inscribir estudiante a una actividad
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
        # para fijar el estado tengo que verifcar que la act. este abierta y que tenga cupos disponibles.
        #consulta sql: revisa cant de inscptos acutalmente con el id de la act.
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

        if actividad[0] != 'abierta': #actividad [0] = estado (orden del select)
            print("La actividad no está abierta, por ende no se puede realizar la inscripción. ")
            return

        estado = 'confirmada' if actividad[2] < actividad[1] else 'lista_espera' #actividad[2] = inscriptos, y [1] cupo max


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


def listar_inscripciones():
    print("\n--- Listado de inscripciones ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
                    SELECT 
                        i.id_inscripcion, i.id_estudiante, i.id_actividad_deportiva, i.fecha_inscripcion, i.estado
                    FROM inscripciones i
                    ORDER BY  i.id_inscripcion;
                """

        cursor.execute(sql)
        encontro = False
        for inscripcion in cursor:
            encontro = False
            print(f"ID Inscripción: {inscripcion[0]} | ID Estudiante: {inscripcion[1]} | ID Actividad Deportiva: {inscripcion[2]} | Fecha: {inscripcion[3]} | Estado: {inscripcion[4]}")

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