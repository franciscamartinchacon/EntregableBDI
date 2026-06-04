USE entregablebd1;

-- 5. Porcentaje de ocupación de cada actividad
SELECT a.id_actividad, a.nombre, a.cupo_max, COUNT(i.id_inscripcion) AS confirmados
FROM actividadesDeportivas a
LEFT JOIN inscripciones i
    ON a.id_actividad = i.id_actividad_deportiva
    AND i.estado = 'confirmada'
GROUP BY a.id_actividad, a.nombre, a.cupo_max
ORDER BY ROUND(((confirmados / a.cupo_max) * 100),2) DESC;    -- Para que muestre solo dos decimales

-- 6. Porcentaje de asistencia por actividad




-- 7. Estudiantes con tres o más inasistencias registradas
SELECT e.id_estudiante, e.documento, e.nombre, e.apellido, COUNT(asis.id_asistencia) AS cantidad_inasistencias
FROM estudiantes e
JOIN inscripciones i on e.id_estudiante = i.id_estudiante
JOIN asistencias asis on i.id_inscripcion = asis.id_inscripcion
WHERE asis.presente = FALSE
GROUP BY e.id_estudiante, e.documento, e.nombre, e.apellido
HAVING cantidad_inasistencias >= 3
ORDER BY cantidad_inasistencias DESC;

