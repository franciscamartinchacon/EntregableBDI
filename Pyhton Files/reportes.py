from conexionSQL import get_connection
from validacion_datos import presione_enter

#despliega un menu con las consultas
def menu_reportes():
    while True:
        print("\n--- Consultar Reportes ---")
        print("1. Actividades con mayor cantidad de inscriptos confirmados.")
        print("2. Actividades con cupos disponibles.")
        print("3. Cantidad de inscriptos por disciplina deportiva.")
        print("4. Cantidad de inscriptos por carrera/facultad")
        print("5. Porcentaje de ocupación de cada actividad.")
        print("6. Porcentaje de asistencia por actividad.")
        print("7. Estudiantes con tres o más inasistencias registradas.")
        print("8. Estudiantes en lista de espera por actividad.")
        print("9. Actividades con mayor porcentaje de asistencia que el promedio.")
        print("10. Actividades que existen pero no tienen estudiantes confirmados.")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        if opcion == "0":
            print("Saliendo...")
            break

        conexion = None
        cursor = None

        try:
            conexion = get_connection()
            cursor = conexion.cursor()

            if opcion == "1":
                query = """
                SELECT a.id_actividad, a.nombre, COUNT(i.id_inscripcion) as cant_inscripciones
                FROM actividadesDeportivas a
                JOIN inscripciones i ON a.id_actividad = i.id_actividad
                WHERE i.estado = 'confirmada'
                GROUP BY a.id_actividad, a.nombre
                ORDER BY cant_inscripciones DESC
                Limit 3;
                """

                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay estudiantes inscriptos en actividades.")
                else:
                    print("Actividades con mayor cantidad de inscriptos confirmados.")
                    for consulta in consultas:
                        print(
                            f"ID Actividad: {consulta[0]} | "
                            f"Nombre: {consulta[1]} | "
                            f"Cantidad de inscripciones: {consulta[2]} | "
                        )


            elif opcion == "2":
                query = """
                SELECT a.id_actividad, a.nombre, a.estado, (SELECT a.cupo_max - COUNT(*) FROM inscripciones i WHERE i.id_actividad= a.id_actividad AND i.estado = 'confirmada') as cant_cupos_disponibles  -- subconslta
                FROM actividadesDeportivas a
                WHERE a.cupo_max > (SELECT COUNT(*) FROM inscripciones i WHERE i.id_actividad = a.id_actividad AND i.estado = 'confirmada')
                ORDER BY cant_cupos_disponibles DESC;
                """

                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay actividades con cupos disponibles.")
                else:
                    print("Actividades con cupos disponibles.")
                    for consulta in consultas:
                        print(
                            f"ID Activdad: {consulta[0]} | "
                            f"Nombre: {consulta[1]} | "
                            f"Estado: {consulta[2]} | "
                            f"Cupos disponibles: {consulta[3]}"
                        )

            elif opcion == "3":
                query = """
                SELECT COUNT(I.id_inscripcion) as cant_inscriptos, d.nombre
                FROM inscripciones i
                RIGHT JOIN actividadesDeportivas a on i.id_actividad = a.id_actividad
                RIGHT JOIN disciplinas d on a.id_disciplina = d.id_disciplina AND i.estado = 'confirmada'
                GROUP BY d.nombre
                ORDER BY cant_inscriptos DESC;
                """

                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay estudiantes inscriptos.")
                else:
                    print("Cantidad de inscriptos por disciplina deportiva.")
                    for consulta in consultas:
                        print(
                            f"Cantidad de inscriptos: {consulta[0]} | "
                            f"Nombre: {consulta[1]} | "
                        )

            elif opcion == "4":
                consulta4()

            elif opcion == "5":
                query = """
                SELECT a.id_actividad, a.nombre, a.cupo_max, COUNT(i.id_inscripcion) AS confirmados, ROUND((COUNT(i.id_inscripcion) / a.cupo_max) * 100, 2) AS porcentaje_ocupacion
                FROM actividadesDeportivas a
                         LEFT JOIN inscripciones i ON a.id_actividad = i.id_actividad
                    AND i.estado = 'confirmada'
                GROUP BY a.id_actividad, a.nombre, a.cupo_max
                ORDER BY porcentaje_ocupacion DESC;
                """

                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay registros para realizar el cálculo.")
                else:
                    print("Porcentaje de ocupación de cada actividad.")

                    for consulta in consultas:
                        print(
                            f"ID Actividad: {consulta[0]} | "
                            f"Nombre: {consulta[1]} | "
                            f"Cupo máx.: {consulta[2]} | "
                            f"Confirmados: {consulta[3]} | "
                            f"Porcentaje ocupación: {consulta[4]}"
                        )

            elif opcion == "6":
                query = """
                SELECT a.nombre, ROUND(AVG(asis.presente) * 100, 2) AS porcentaje
                FROM actividadesDeportivas a
                LEFT JOIN inscripciones i ON i.id_actividad = a.id_actividad -- para incluir de cero tambien
                LEFT JOIN asistencias asis ON i.id_inscripcion = asis.id_inscripcion AND i.estado = 'confirmada'
                GROUP BY a.nombre
                ORDER BY porcentaje DESC;
                """
                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay registros para realizar el cálculo.")
                else:
                    print("Porcentaje de asistencia por actividad.")
                    for consulta in consultas:
                        print(
                            f"Nombre: {consulta[0]} | "
                            f"Porcentaje: {consulta[1]} | "
                        )


            elif opcion == "7":
                query = """
                SELECT e.documento, e.nombre, e.apellido, COUNT(asis.id_asistencia) AS cantidad_inasistencias
                FROM estudiantes e
                JOIN inscripciones i on e.documento = i.documento
                JOIN asistencias asis on i.id_inscripcion = asis.id_inscripcion
                WHERE asis.presente = FALSE
                GROUP BY e.documento, e.nombre, e.apellido
                HAVING cantidad_inasistencias >= 3
                ORDER BY cantidad_inasistencias DESC;
                """

                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay inscripciones para realizar el cálculo.")
                else:
                    print("Estudiantes con tres o más inasistencias registradas.")
                    for consulta in consultas:
                        print(
                            f"Documento {consulta[0]} | "
                            f"Nombre: {consulta[1]} | "
                            f"Apellido: {consulta[2]} | "
                            f"Cantidad de inasistencias: {consulta[3]}"
                        )

            elif opcion == "8":
                query = """
                SELECT a.nombre AS actividad, e.nombre, e.apellido, e.documento, i.fecha_inscripcion
                FROM inscripciones i
                JOIN estudiantes e ON i.documento = e.documento
                JOIN actividadesDeportivas a ON i.id_actividad = a.id_actividad
                WHERE i.estado = 'lista_espera'
                ORDER BY a.nombre, i.fecha_inscripcion;
                """
                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay estudiantes registrados.")
                else:
                    print("Estudiantes en lista de espera por actividad..")
                    for consulta in consultas:
                        print(
                            f"Actividad: {consulta[0]} | "
                            f"Nombre: {consulta[1]} | "
                            f"Apellido: {consulta[2]} | "
                            f"Documento: {consulta[3]} | "
                            f"Fecha de inscripción: {consulta[4]}"
                        )

            elif opcion == "9":
                query = """
                SELECT a.id_actividad, a.nombre AS actividad, ROUND(AVG(asis.presente) * 100, 2) AS porcentaje_asistencia
                FROM actividadesDeportivas a
                         JOIN inscripciones i ON a.id_actividad = i.id_actividad
                         JOIN asistencias asis ON i.id_inscripcion = asis.id_inscripcion
                WHERE i.estado = 'confirmada'
                GROUP BY a.id_actividad, a.nombre
                HAVING porcentaje_asistencia > (
                    SELECT AVG(porcentaje)
                    FROM (
                             SELECT AVG(asis2.presente) * 100 AS porcentaje
                             FROM actividadesDeportivas a2
                                      JOIN inscripciones i2 ON a2.id_actividad = i2.id_actividad
                                      JOIN asistencias asis2 ON i2.id_inscripcion = asis2.id_inscripcion
                             WHERE i2.estado = 'confirmada'
                             GROUP BY a2.id_actividad
                         ) AS porcentajes_por_actividad
                )
                ORDER BY porcentaje_asistencia DESC;
                """

                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay estudiantes registrados.")
                else:
                    print("Actividades con mayor porcentaje de asistencia que el promedio.")
                    for consulta in consultas:
                        print(
                            f"ID Actividad: {consulta[0]} | "
                            f"Actividad: {consulta[1]} | "
                            f"Porcentaje Asistencia: {consulta[2]}"
                        )


            elif opcion == "10":
                query = """
                SELECT a.id_actividad, a.nombre AS actividad, d.nombre AS disciplina, a.fecha, a.hora_inicio, a.hora_fin, a.estado
                FROM actividadesDeportivas a
                         JOIN disciplinas d ON a.id_disciplina = d.id_disciplina
                         LEFT JOIN inscripciones i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
                WHERE i.id_inscripcion IS NULL
                ORDER BY a.fecha, a.hora_inicio;
                """
                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay estudiantes registrados.")
                else:
                    print("Actividades que existen pero no tienen estudiantes confirmados")
                    for consulta in consultas:
                        print(
                            f"ID Actividad: {consulta[0]} | "
                            f"Actividad: {consulta[1]} | "
                            f"Disciplina: {consulta[2]} | "
                            f"Fecha: {consulta[3]} | " 
                            f"Horario: {consulta[4]} a {consulta[5]} | "
                            f"Estado: {consulta[6]}"
                        )

            else:
                print("Opción inválida. Intente nuevamente.")

        except Exception as e:
            print("Error al ejecutar el reporte:")
            print(e)

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

        presione_enter()


def consulta4():
    while True:
        print("\n--- Consultas posibles (4) ---")
        print("1. Cantidad de inscriptos por carrera.")
        print("2. Cantidad de inscriptos por facultad.")
        print("0. Volver al menu anterior")

        opcion = input("Seleccione una opción: ")

        if opcion == "0":
            break

        conexion = None
        cursor = None

        try:
            conexion = get_connection()
            cursor = conexion.cursor()

            if opcion == "1":
                query = """
                SELECT COUNT(*) cant_inscriptos, c.nombre
                FROM inscripciones i
                JOIN estudiantes e on i.documento = e.documento
                JOIN carreras c on e.id_carrera = c.id_carrera
                WHERE i.estado = 'confirmada'
                GROUP BY c.nombre;
                """

                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay estudiantes registrados.")
                else:
                    print("Cantidad de inscriptos por carrera.")
                    for consulta in consultas:
                        print(
                            f"Cantidad de inscriptos: {consulta[0]} | "
                            f"Carrera: {consulta[1]}"
                        )

            elif opcion == "2":
                query = """
                SELECT COUNT(*) cant_inscriptos, f.nombre
                FROM inscripciones i
                JOIN estudiantes e on i.documento = e.documento
                JOIN carreras c on e.id_carrera = c.id_carrera
                JOIN facultades f on c.id_facultad = f.id_facultad
                WHERE i.estado = 'confirmada'
                GROUP BY f.nombre;
                """

                cursor.execute(query)
                consultas = cursor.fetchall()

                if len(consultas) == 0:
                    print("No hay estudiantes registrados.")
                else:
                    print("Cantidad de inscriptos por facultad.")
                    for consulta in consultas:
                        print(
                            f"Cantidad de inscriptos: {consulta[0]} | "
                            f"Facultad: {consulta[1]}"
                        )

            else:
                print("Opción inválida. Intente nuevamente.")

        except Exception as e:
            print("Error al ejecutar la consulta:")
            print(e)

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

        presione_enter()