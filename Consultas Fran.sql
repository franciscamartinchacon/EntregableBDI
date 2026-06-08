USE entregablebd1;

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
JOIN inscripciones i ON i.id_actividad_deportiva = a.id_actividad
JOIN asistencias asis ON i.id_inscripcion = asis.id_inscripcion
WHERE i.estado = 'confirmada'
GROUP BY a.nombre
ORDER BY porcentaje DESC;

-- 7. Estudiantes con tres o más inasistencias registradas
SELECT e.id_estudiante, e.documento, e.nombre, e.apellido, COUNT(asis.id_asistencia) AS cantidad_inasistencias
FROM estudiantes e
JOIN inscripciones i on e.id_estudiante = i.id_estudiante
JOIN asistencias asis on i.id_inscripcion = asis.id_inscripcion
WHERE asis.presente = FALSE
GROUP BY e.id_estudiante, e.documento, e.nombre, e.apellido
HAVING cantidad_inasistencias >= 3
ORDER BY cantidad_inasistencias DESC;

-- 8. Estudiantes en lista de espera por actividad
SELECT a.nombre AS actividad, e.nombre, e.apellido, e.documento, i.fecha_inscripcion
FROM inscripciones i
JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
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

-- 10.
