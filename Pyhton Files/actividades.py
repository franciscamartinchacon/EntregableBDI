from conexionSQL import get_connection
from validacion_datos import pedir_texto_obligatorio, pedir_entero, pedir_entero_positivo, pedir_opcion_valida, presione_enter
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
            presione_enter()
        elif opcion == "2":
            listar_actividades()
            presione_enter()
        elif opcion == "3":
            modificar_actividad()
            presione_enter()
        elif opcion == "4":
            eliminar_actividad()
            presione_enter()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


def listar_docentes():
    print("\n--- Docentes disponibles ---")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            SELECT documento, nombre, apellido
            FROM docentes
            ORDER BY apellido, nombre;
        """

        cursor.execute(sql)
        docentes = cursor.fetchall()

        if len(docentes) == 0:
            print("No hay docentes registrados.")
        else:
            for docente in docentes:
                print(
                    f"Documento: {docente[0]} | "
                    f"Docente: {docente[1]} {docente[2]}"
                )

    except Exception as e:
        print("Error al listar docentes:")
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

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
        "Día de la semana (lunes, martes, miercoles, jueves, viernes, sabado, domingo): ",
        dias_validos
    )

    fecha = pedir_texto_obligatorio("Fecha (AAAA-MM-DD): ")
    hora_inicio = pedir_texto_obligatorio("Hora de inicio (HH:MM:SS): ")
    hora_fin = pedir_texto_obligatorio("Hora de fin (HH:MM:SS): ")

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

    print("\nSeleccione un docente:")
    listar_docentes()
    docente_asignado = pedir_entero("Ingrese el documento del docente asignado: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO actividadesDeportivas
            (nombre, id_disciplina, id_espacio, cupo_max, dia_semana, fecha, hora_inicio, hora_fin, estado, docente_asignado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        valores = (
            nombre,
            id_disciplina,
            id_espacio,
            cupo_max,
            dia_semana,
            fecha,
            hora_inicio,
            hora_fin,
            estado,
            docente_asignado
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
            SELECT 
                a.id_actividad, 
                a.nombre, 
                d.nombre AS disciplina, 
                e.nombre AS espacio, 
                e.ubicacion, 
                a.cupo_max, 
                a.dia_semana, 
                a.fecha, 
                a.hora_inicio, 
                a.hora_fin, 
                a.estado,
                doc.nombre, 
                doc.apellido
                
            FROM actividadesDeportivas a
            JOIN disciplinas d ON a.id_disciplina = d.id_disciplina
            JOIN espaciosDeportivos e ON a.id_espacio = e.id_espacio
            JOIN docentes doc ON a.docente_asignado = doc.documento
            ORDER BY a.fecha, a.hora_inicio;
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
                    f"Hora_inicio: {actividad[8]} | "
                    f"Hora_fin: {actividad[9]} | "
                    f"Estado: {actividad[10]}"
                    f"Docente: {actividad[11]} {actividad[12]}"
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

    while True:
        print("\n--- Ingrese el dato que quiere modificar ---")
        print("1. Nombre")
        print("2. Disciplina")
        print("3. Espacio deportivo")
        print("4. Cupo máximo")
        print("5. Día de la semana")
        print("6. Fecha")
        print("7. Hora inicio")
        print("8. Estado")
        print("9. Docente")
        print("0. Volver al menú de actividades")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            modificar_nombre_actividad(id_actividad)
        elif opcion == "2":
            modificar_disciplina_actividad(id_actividad)
        elif opcion == "3":
            modificar_espacio_actividad(id_actividad)
        elif opcion == "4":
            modificar_cupo_actividad(id_actividad)
        elif opcion == "5":
            modificar_dia_actividad(id_actividad)
        elif opcion == "6":
            modificar_fecha_actividad(id_actividad)
        elif opcion == "7":
            modificar_horario_actividad(id_actividad)
        elif opcion == "8":
            modificar_estado_actividad(id_actividad)
        elif opcion == "9":
            modificar_docente_actividad(id_actividad)
        elif opcion == "0":
            print("Volviendo al menú de actividades...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

def modificar_nombre_actividad(id_actividad):

        nombre = pedir_texto_obligatorio("Nuevo nombre: ")

        conexion = None
        cursor = None

        try:
            conexion = get_connection()
            cursor = conexion.cursor()

            sql = """
                UPDATE actividadesDeportivas
                SET nombre = %s
                WHERE id_actividad = %s;
            """

            cursor.execute(sql, (nombre, id_actividad))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Nombre de actividad modificado correctamente.")
            else:
                print("No se encontró una actividad con ese ID.")

        except Exception as e:
            print("Error al modificar el nombre de la actividad:")
            print(e)

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

def modificar_disciplina_actividad(id_actividad):

        print("\nSeleccione la nueva disciplina:")
        listar_disciplinas()

        id_disciplina = pedir_entero("Nuevo ID de disciplina: ")

        conexion = None
        cursor = None

        try:
            conexion = get_connection()
            cursor = conexion.cursor()

            sql = """
                UPDATE actividadesDeportivas
                SET id_disciplina = %s
                WHERE id_actividad = %s;
            """

            cursor.execute(sql, (id_disciplina, id_actividad))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Disciplina de la actividad modificada correctamente.")
            else:
                print("No se encontró una actividad con ese ID.")

        except Exception as e:
            print("Error al modificar la disciplina de la actividad:")
            print(e)
            print("Puede ser que no exista una disciplina con ese ID.")

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

def modificar_espacio_actividad(id_actividad):

        print("\nSeleccione el nuevo espacio deportivo:")
        listar_espacios()

        id_espacio = pedir_entero("Nuevo ID de espacio deportivo: ")

        conexion = None
        cursor = None

        try:
            conexion = get_connection()
            cursor = conexion.cursor()

            sql = """
                UPDATE actividadesDeportivas
                SET id_espacio = %s
                WHERE id_actividad = %s;
            """

            cursor.execute(sql, (id_espacio, id_actividad))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Espacio de la actividad modificado correctamente.")
            else:
                print("No se encontró una actividad con ese ID.")

        except Exception as e:
            print("Error al modificar el espacio de la actividad:")
            print(e)
            print("Puede ser que no exista un espacio con ese ID.")

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

def modificar_cupo_actividad(id_actividad):

        cupo_max = pedir_entero_positivo("Nuevo cupo máximo: ")

        conexion = None
        cursor = None

        try:
            conexion = get_connection()
            cursor = conexion.cursor()

            sql = """
                UPDATE actividadesDeportivas
                SET cupo_max = %s
                WHERE id_actividad = %s;
            """

            cursor.execute(sql, (cupo_max, id_actividad))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Cupo máximo modificado correctamente.")
            else:
                print("No se encontró una actividad con ese ID.")

        except Exception as e:
            print("Error al modificar el cupo máximo:")
            print(e)

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

def modificar_dia_actividad(id_actividad):

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
            "Nuevo día de la semana (lunes, martes, miercoles, jueves, viernes, sabado, domingo): ",
            dias_validos
        )

        conexion = None
        cursor = None

        try:
            conexion = get_connection()
            cursor = conexion.cursor()

            sql = """
                UPDATE actividadesDeportivas
                SET dia_semana = %s
                WHERE id_actividad = %s;
            """

            cursor.execute(sql, (dia_semana, id_actividad))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Día de la actividad modificado correctamente.")
            else:
                print("No se encontró una actividad con ese ID.")

        except Exception as e:
            print("Error al modificar el día de la actividad:")
            print(e)

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

def modificar_fecha_actividad(id_actividad):

        fecha = pedir_texto_obligatorio("Nueva fecha (AAAA-MM-DD): ")

        conexion = None
        cursor = None

        try:
            conexion = get_connection()
            cursor = conexion.cursor()

            sql = """
                UPDATE actividadesDeportivas
                SET fecha = %s
                WHERE id_actividad = %s;
            """

            cursor.execute(sql, (fecha, id_actividad))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Fecha de la actividad modificada correctamente.")
            else:
                print("No se encontró una actividad con ese ID.")

        except Exception as e:
            print("Error al modificar la fecha de la actividad:")
            print(e)
            print("Revise que la fecha tenga formato AAAA-MM-DD.")

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

def modificar_horario_actividad(id_actividad):
    #Modifica la hora de inicio y la hora de fin de una actividad deportiva.

    hora_inicio = pedir_texto_obligatorio("Nueva hora de inicio (HH:MM:SS): ")
    hora_fin = pedir_texto_obligatorio("Nueva hora de fin (HH:MM:SS): ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE actividadesDeportivas
            SET hora_inicio = %s,
                hora_fin = %s
            WHERE id_actividad = %s;
        """

        cursor.execute(sql, (hora_inicio, hora_fin, id_actividad))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Horario de la actividad modificado correctamente.")
        else:
            print("No se encontró una actividad con ese ID.")

    except Exception as e:
        print("Error al modificar el horario de la actividad:")
        print(e)
        print("Revise que las horas tengan formato HH:MM:SS y que la hora de fin sea mayor a la hora de inicio.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def modificar_estado_actividad(id_actividad):

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
                SET estado = %s
                WHERE id_actividad = %s;
            """

            cursor.execute(sql, (estado, id_actividad))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Estado de la actividad modificado correctamente.")
            else:
                print("No se encontró una actividad con ese ID.")

        except Exception as e:
            print("Error al modificar el estado de la actividad:")
            print(e)

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

def modificar_docente_actividad(id_actividad):

    print("\nSeleccione el nuevo docente:")
    listar_docentes()

    docente_asignado = pedir_entero("Nuevo documento del docente asignado: ")

    conexion = None
    cursor = None

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE actividadesDeportivas
            SET docente_asignado = %s
            WHERE id_actividad = %s;
        """

        cursor.execute(sql, (docente_asignado, id_actividad))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Docente asignado modificado correctamente.")
        else:
            print("No se encontró una actividad con ese ID.")

    except Exception as e:
        print("Error al modificar el docente asignado:")
        print(e)
        print("Puede ser que no exista un docente con ese documento.")

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def eliminar_actividad():

    print("\n--- Eliminar actividad deportiva ---")

    listar_actividades()

    id_actividad = pedir_entero("\nIngrese el ID de la actividad a eliminar: ")

    confirmacion = input("¿Seguro que desea eliminar esta actividad? (si/no): ").strip().lower()

    if confirmacion != "si":
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
