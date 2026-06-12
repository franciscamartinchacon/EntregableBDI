USE entregablebd1;

-- Cosnultas requeridas
-- 1. Actividades con mayor cantidad de inscriptos confirmados.
SELECT a.id_actividad, a.nombre, COUNT(*) as cant_inscripciones
FROM actividadesDeportivas a
JOIN inscripciones i ON a.id_actividad = i.id_actividad_deportiva
GROUP BY a.id_actividad, a.nombre
ORDER BY cant_inscripciones DESC
Limit 3; -- para que no devuelva una sola, sino el top 3

-- 2. Actividades con cupos disponibles.
SELECT a.id_actividad, a.nombre, a.estado, (SELECT a.cupo_max - COUNT(*) FROM inscripciones i WHERE i.id_actividad_deportiva = a.id_actividad AND i.estado = 'confirmada') as cant_cupos_disponibles  -- subconslta
FROM actividadesDeportivas a
WHERE a.cupo_max > (SELECT COUNT(*) FROM inscripciones i WHERE i.id_actividad_deportiva = a.id_actividad AND i.estado = 'confirmada')
ORDER BY cant_cupos_disponibles DESC; #deberia filtar solo actividades abiertas??

-- 3. Cantidad de inscriptos por disciplina deportiva.
SELECT COUNT(I.id_inscripcion) as cant_inscriptos, d.nombre
FROM inscripciones i
RIGHT JOIN actividadesDeportivas a on i.id_actividad_deportiva = a.id_actividad
RIGHT JOIN disciplinas d on a.id_disciplina = d.id_disciplina AND i.estado = 'confirmada'
GROUP BY d.nombre
ORDER BY cant_inscriptos DESC;

-- 4.1 Cantidad de inscriptos por carrera
SELECT COUNT(*) cant_inscriptos, c.nombre
FROM inscripciones i
JOIN estudiantes e on i.documento = e.documento
JOIN carreras c on e.id_carrera = c.id_carrera
WHERE i.estado = 'confirmada'
GROUP BY c.nombre;

-- 4.2 Cantidad de inscriptos por facultad
SELECT COUNT(*) cant_inscriptos, f.nombre
FROM inscripciones i
JOIN estudiantes e on i.documento = e.documento
JOIN carreras c on e.id_carrera = c.id_carrera
JOIN facultades f on c.id_facultad = f.id_facultad
WHERE i.estado = 'confirmada'
GROUP BY f.nombre;

-- 5. Porcentaje de ocupación de cada actividad
SELECT a.id_actividad, a.nombre, a.cupo_max, COUNT(i.id_inscripcion) AS confirmados, ROUND((COUNT(i.id_inscripcion) / a.cupo_max) * 100, 2) AS porcentaje_ocupacion
FROM actividadesDeportivas a
         LEFT JOIN inscripciones i ON a.id_actividad = i.id_actividad_deportiva
    AND i.estado = 'confirmada'
GROUP BY a.id_actividad, a.nombre, a.cupo_max
ORDER BY porcentaje_ocupacion DESC;

-- 6. Porcentaje de asistencia por actividad
SELECT a.nombre, ROUND(AVG(asis.presente) * 100, 2) AS porcentaje
FROM actividadesDeportivas a
LEFT JOIN inscripciones i ON i.id_actividad_deportiva = a.id_actividad -- para inculir de cero tambien
LEFT JOIN asistencias asis ON i.id_inscripcion = asis.id_inscripcion AND i.estado = 'confirmada'
GROUP BY a.nombre
ORDER BY porcentaje DESC;

-- 7. Estudiantes con tres o más inasistencias registradas
SELECT e.documento, e.nombre, e.apellido, COUNT(asis.id_asistencia) AS cantidad_inasistencias
FROM estudiantes e
JOIN inscripciones i on e.documento = i.documento
JOIN asistencias asis on i.id_inscripcion = asis.id_inscripcion
WHERE asis.presente = FALSE
GROUP BY e.documento, e.nombre, e.apellido
HAVING cantidad_inasistencias >= 3
ORDER BY cantidad_inasistencias DESC;

-- 8. Estudiantes en lista de espera por actividad
-- VER ORDER BY (ACTIVIDAD?) Y DSP CAMBIAR EN PYTHON
SELECT a.nombre AS actividad, e.nombre, e.apellido, e.documento, i.fecha_inscripcion
FROM inscripciones i
 JOIN estudiantes e ON i.documento = e.documento
 JOIN actividadesDeportivas a ON i.id_actividad_deportiva = a.id_actividad
WHERE i.estado = 'lista_espera'
ORDER BY a.nombre, i.fecha_inscripcion;

-- 9. Actividades con mayor porcentaje de asistencia que el promedio
SELECT a.id_actividad, a.nombre AS actividad, ROUND(AVG(asis.presente) * 100, 2) AS porcentaje_asistencia
FROM actividadesDeportivas a
         JOIN inscripciones i ON a.id_actividad = i.id_actividad_deportiva
         JOIN asistencias asis ON i.id_inscripcion = asis.id_inscripcion
WHERE i.estado = 'confirmada'
GROUP BY a.id_actividad, a.nombre
HAVING porcentaje_asistencia > (
    SELECT AVG(porcentaje)
    FROM (
             SELECT AVG(asis2.presente) * 100 AS porcentaje
             FROM actividadesDeportivas a2
                      JOIN inscripciones i2 ON a2.id_actividad = i2.id_actividad_deportiva
                      JOIN asistencias asis2 ON i2.id_inscripcion = asis2.id_inscripcion
             WHERE i2.estado = 'confirmada'
             GROUP BY a2.id_actividad
         ) AS porcentajes_por_actividad
)
ORDER BY porcentaje_asistencia DESC;

-- 10. Actividades que existen pero no tienen estudiantes confirmados
SELECT a.id_actividad, a.nombre AS actividad, d.nombre AS disciplina, a.fecha, a.horario, a.estado
FROM actividadesDeportivas a
         JOIN disciplinas d ON a.id_disciplina = d.id_disciplina
         LEFT JOIN inscripciones i ON a.id_actividad = i.id_actividad_deportiva AND i.estado = 'confirmada'
WHERE i.id_inscripcion IS NULL
ORDER BY a.fecha, a.horario;
