from conexionSQL import get_connection
from validacion_datos import pedir_texto_obligatorio, pedir_entero, pedir_entero_positivo, pedir_opcion_valida
from disciplinas import listar_disciplinas
from espacios import listar_espacios

def menu_actividades():

    while True:
        print("\n--- ABM Actividades Deportivas ---")
        print("1. Alta actividad deportiva")
        print("2. Listar actividades deportivas")
        print("3. Modificar actividad deportiva")
        print("4. Eliminar actividad deportiva")
        print("5. Cambiar estado de actividad")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            alta_actividad()
        elif opcion == "2":
            listar_actividades()
        elif opcion == "3":
            modificar_actividad()
        elif opcion == "4":
            eliminar_actividad()
        elif opcion == "5":
            cambiar_estado_actividad()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


def alta_actividad():

    print("\n--- Alta de actividad deportiva ---")

    nombre = pedir_texto_obligatorio("Nombre de la actividad: ")

    print("\nSeleccione una disciplina:")
    listar_disciplinas()
    id_disciplina = pedir_entero("Ingrese el ID de la disciplina: ")

    print("\nSeleccione un espacio deportivo:")
    listar_espacios()
    id_espacio = pedir_entero("Ingrese el ID del espacio deportivo: ")

    cupo_max = pedir_entero_positivo("Cupo máximo: ")

    dias_validos = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo"
    ]

    dia_semana = pedir_opcion_valida(
        "Día de la semana: ",
        dias_validos
    )

    fecha = pedir_texto_obligatorio("Fecha (AAAA-MM-DD): ")
    horario = pedir_texto_obligatorio("Horario (HH:MM:SS): ")

    estados_validos = [
        "abierta",
        "cerrada",
        "finalizada",
        "cancelada"
    ]

    estado = pedir_opcion_valida(
        "Estado (abierta/cerrada/finalizada/cancelada): ",
        estados_validos
    )

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO actividadesDeportivas
            (nombre, id_disciplina, id_espacio, cupo_max, dia_semana, fecha, horario, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        valores = (
            nombre,
            id_disciplina,
            id_espacio,
            cupo_max,
            dia_semana,
            fecha,
            horario,
            estado
        )

        cursor.execute(sql, valores)
        conexion.commit()

        print("Actividad deportiva creada correctamente.")

    except Exception as e:
        print("Error al crear la actividad deportiva.")
        print(e)
        print("Revise que la disciplina y el espacio existan, y que los datos ingresados sean válidos.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def listar_actividades():

    print("\n--- Listado de actividades deportivas ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT a.id_actividad, a.nombre, d.nombre AS disciplina, e.nombre AS espacio, e.ubicacion, a.cupo_max, a.dia_semana, a.fecha, a.horario, a.estado
            FROM actividadesDeportivas a
            JOIN disciplinas d
                ON a.id_disciplina = d.id_disciplina
            JOIN espaciosDeportivos e
                ON a.id_espacio = e.id_espacio
            ORDER BY a.fecha, a.horario;
        """

        cursor.execute(sql)
        actividades = cursor.fetchall()

        if len(actividades) == 0:
            print("No hay actividades deportivas registradas.")
        else:
            for actividad in actividades:
                print(
                    f"ID: {actividad[0]} | "
                    f"Actividad: {actividad[1]} | "
                    f"Disciplina: {actividad[2]} | "
                    f"Espacio: {actividad[3]} | "
                    f"Ubicación: {actividad[4]} | "
                    f"Cupo máximo: {actividad[5]} | "
                    f"Día: {actividad[6]} | "
                    f"Fecha: {actividad[7]} | "
                    f"Horario: {actividad[8]} | "
                    f"Estado: {actividad[9]}"
                )

    except Exception as e:
        print("Error al listar actividades deportivas.")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def modificar_actividad():

    print("\n--- Modificar actividad deportiva ---")

    listar_actividades()

    id_actividad = pedir_entero("\nIngrese el ID de la actividad a modificar: ")

    print("\nIngrese los nuevos datos de la actividad:")

    nombre = pedir_texto_obligatorio("Nuevo nombre: ")

    print("\nSeleccione la nueva disciplina:")
    listar_disciplinas()
    id_disciplina = pedir_entero("Nuevo ID de disciplina: ")

    print("\nSeleccione el nuevo espacio deportivo:")
    listar_espacios()
    id_espacio = pedir_entero("Nuevo ID de espacio deportivo: ")

    cupo_max = pedir_entero_positivo("Nuevo cupo máximo: ")

    dias_validos = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo"
    ]

    dia_semana = pedir_opcion_valida(
        "Nuevo día de la semana: ",
        dias_validos
    )

    fecha = pedir_texto_obligatorio("Nueva fecha (AAAA-MM-DD): ")
    horario = pedir_texto_obligatorio("Nuevo horario (HH:MM:SS): ")

    estados_validos = [
        "abierta",
        "cerrada",
        "finalizada",
        "cancelada"
    ]

    estado = pedir_opcion_valida(
        "Nuevo estado (abierta/cerrada/finalizada/cancelada): ",
        estados_validos
    )

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE actividadesDeportivas
            SET nombre = %s,
                id_disciplina = %s,
                id_espacio = %s,
                cupo_max = %s,
                dia_semana = %s,
                fecha = %s,
                horario = %s,
                estado = %s
            WHERE id_actividad = %s;
        """

        valores = (
            nombre,
            id_disciplina,
            id_espacio,
            cupo_max,
            dia_semana,
            fecha,
            horario,
            estado,
            id_actividad
        )

        cursor.execute(sql, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print("Actividad deportiva modificada correctamente.")
        else:
            print("No se encontró una actividad con ese ID.")

    except Exception as e:
        print("Error al modificar la actividad deportiva.")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def eliminar_actividad():

    print("\n--- Eliminar actividad deportiva ---")

    listar_actividades()

    id_actividad = pedir_entero("\nIngrese el ID de la actividad a eliminar: ")

    confirmacion = input("¿Seguro que desea eliminar esta actividad? (s/n): ").strip().lower()

    if confirmacion != "s":
        print("Operación cancelada.")
        return

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            DELETE FROM actividadesDeportivas
            WHERE id_actividad = %s;
        """

        cursor.execute(sql, (id_actividad,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Actividad deportiva eliminada correctamente.")
        else:
            print("No se encontró una actividad con ese ID.")

    except Exception as e:
        print("Error al eliminar la actividad deportiva.")
        print(e)
        print("Puede ser que la actividad tenga inscripciones asociadas.")
        print("En ese caso, use la opción 'Cambiar estado de actividad' y seleccione 'cancelada'.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def cambiar_estado_actividad():

    print("\n--- Cambiar estado de actividad ---")

    listar_actividades()

    id_actividad = pedir_entero("\nIngrese el ID de la actividad: ")

    estados_validos = [
        "abierta",
        "cerrada",
        "finalizada",
        "cancelada"
    ]

    nuevo_estado = pedir_opcion_valida(
        "Nuevo estado (abierta/cerrada/finalizada/cancelada): ",
        estados_validos
    )

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE actividadesDeportivas
            SET estado = %s
            WHERE id_actividad = %s;
        """

        cursor.execute(sql, (nuevo_estado, id_actividad))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Estado de la actividad actualizado correctamente.")
        else:
            print("No se encontró una actividad con ese ID.")

    except Exception as e:
        print("Error al cambiar el estado de la actividad.")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()