
from conexionSQL import get_connection
from validacion_datos import pedir_entero, pedir_cedula, presione_enter
from estudiantes import listar_estudiantes
from actividades import listar_actividades

def gestion_inscripciones():
    while True:
        print("\n--- Gestión Inscripciones ---")
        print("1. Inscribir estudiante")
        print("2. Listar inscripciones")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            inscribir_estudiante()
            presione_enter()
        elif opcion == "2":
            listar_inscripciones()
            presione_enter()
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
            JOIN actividadesDeportivas actual ON i.id_actividad = actual.id_actividad
            JOIN actividadesDeportivas nueva ON nueva.id_actividad = %s
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
    documento = pedir_cedula("Ingrese el documento del Estudiante: ")

    listar_actividades()
    id_actividad = pedir_entero("Ingrese el ID de la Actvividad Deportiva: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        #Verificar que el estudiante exista
        sql_estudiante = """
                SELECT COUNT(*)
                FROM estudiantes
                WHERE documento = %s;
            """

        cursor.execute(sql_estudiante, (documento,))
        existe_estudiante = cursor.fetchone()[0]

        if existe_estudiante == 0:
            print("El estudiante no existe.")
            return

        #Verificar que la actividad exista, que esté abierta y contar confirmados
        sql_verificar = """
                SELECT estado, cupo_max (
                        SELECT COUNT(*) 
                        FROM inscripciones 
                        WHERE id_actividad = %s AND estado = 'confirmada') AS inscriptos
                FROM actividadesDeportivas
                WHERE id_actividad = %s;
            """

        cursor.execute(sql_verificar, (id_actividad, id_actividad))
        actividad = cursor.fetchone()

        if actividad is None:
            print("La actividad no existe.")
            return

        if actividad[0] != "abierta":
            print("La actividad no está abierta, por ende no se puede realizar la inscripción.")
            return

        # actividad[0] = estado
        # actividad[1] = cupo_max
        # actividad[2] = cantidad de inscriptos confirmados
        if actividad[2] < actividad[1]:
            estado = "confirmada"
        else:
            estado = "lista_espera"

        #Solo si queda confirmada, controlar que no se pise con otra actividad
        if estado == "confirmada" and tiene_conflicto_horario(documento, id_actividad):
            print("El estudiante ya tiene una actividad confirmada en ese horario.")
            return

        #Insertar inscripción
        sql_insertar = """
                INSERT INTO inscripciones 
                (documento, id_actividad, estado)
                VALUES (%s, %s, %s);
            """

        valores = (documento, id_actividad, estado)

        cursor.execute(sql_insertar, valores)
        conexion.commit()

        if estado == "confirmada":
            print("Inscripción creada correctamente. Estado: confirmada.")
        else:
            print("La actividad no tiene cupos disponibles. El estudiante quedó en lista de espera.")

    except Exception as e:
        print("Error al crear inscripción:")
        print(e)
        print("Puede ser que el estudiante ya esté inscripto a esa actividad o que algún dato no sea válido.")

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
                        i.id_inscripcion, i.documento, e.nombre, e.apellido, i.id_actividad, a.nombre AS actividad, i.fecha_inscripcion, i.estado
                    FROM inscripciones i
                    ORDER BY  i.id_inscripcion;
                """

        cursor.execute(sql)
        inscripciones = cursor.fetchall()

        if len(inscripciones) == 0:
            print("No hay inscripciones cargadas.")
        else:
            for inscripcion in inscripciones:
                print(
                    f"ID Inscripción: {inscripcion[0]} | "
                    f"Documento: {inscripcion[1]} | "
                    f"Estudiante: {inscripcion[2]} {inscripcion[3]} | "
                    f"ID Actividad: {inscripcion[4]} | "
                    f"Actividad: {inscripcion[5]} | "
                    f"Fecha inscripción: {inscripcion[6]} | "
                    f"Estado: {inscripcion[7]}"
                )

    except Exception as e:
        print("Error al listar inscripciones:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def inscribirme_a_actividad(documento):
    print("\n--- Inscribirme a una actividad ---")

    listar_actividades()
    id_actividad = pedir_entero("Ingrese el ID de la actividad deportiva: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        # La actividad tiene que existir y estar abiierta. Cupos ocupados
        sql_verificar = """
            SELECT 
                estado, 
                cupo_max,
                (
                    SELECT COUNT(*) 
                    FROM inscripciones 
                    WHERE id_actividad = %s 
                      AND estado = 'confirmada'
                ) AS inscriptos
            FROM actividadesDeportivas
            WHERE id_actividad = %s;
        """

        cursor.execute(sql_verificar, (id_actividad, id_actividad))
        actividad = cursor.fetchone()

        if actividad is None:
            print("La actividad no existe.")
            return

        if actividad[0] != "abierta":
            print("La actividad no está abierta, por ende no se puede realizar la inscripción.")
            return

        # actividad[1] = cupo_max
        # actividad[2] = inscriptos confirmados
        if actividad[2] < actividad[1]:
            estado = "confirmada"
        else:
            estado = "lista_espera"

        # Solo se controla conflicto horario si la inscripción queda confirmada
        if estado == "confirmada" and tiene_conflicto_horario(documento, id_actividad):
            print("Ya tenés una actividad confirmada en ese horario.")
            return

        sql_insertar = """
            INSERT INTO inscripciones
            (documento, id_actividad, estado)
            VALUES (%s, %s, %s);
        """

        cursor.execute(sql_insertar, (documento, id_actividad, estado))
        conexion.commit()

        if estado == "confirmada":
            print("Inscripción creada correctamente. Estado: confirmada.")
        else:
            print("La actividad no tiene cupos disponibles. Quedaste en lista de espera.")

    except Exception as e:
        print("Error al crear inscripción:")
        print(e)
        print("Puede ser que ya estés inscripto a esa actividad.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def ver_mis_inscripciones(documento):
    print("\n--- Mis inscripciones ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT 
                i.id_inscripcion,
                a.nombre,
                a.fecha,
                a.hora_inicio,
                a.hora_fin,
                i.fecha_inscripcion,
                i.estado
            FROM inscripciones i
            JOIN actividadesDeportivas a 
                ON i.id_actividad = a.id_actividad
            WHERE i.documento = %s
            ORDER BY a.fecha, a.hora_inicio;
        """

        cursor.execute(sql, (documento,))
        inscripciones = cursor.fetchall()

        if len(inscripciones) == 0:
            print("No tenés inscripciones registradas.")
        else:
            for inscripcion in inscripciones:
                print(
                    f"ID inscripción: {inscripcion[0]} | "
                    f"Actividad: {inscripcion[1]} | "
                    f"Fecha actividad: {inscripcion[2]} | "
                    f"Horario: {inscripcion[3]} a {inscripcion[4]} | "
                    f"Fecha inscripción: {inscripcion[5]} | "
                    f"Estado: {inscripcion[6]}"
                )

    except Exception as e:
        print("Error al listar tus inscripciones:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()