USE entregablebd1;

-- Cosnultas requeridas
-- 1. Actividades con mayor cantidad de inscriptos confirmados.
SELECT a.id_actividad, a.nombre, COUNT(*) as cant_inscripciones
FROM actividadesDeportivas a
JOIN inscripciones i ON a.id_actividad = i.id_actividad_deportiva
GROUP BY a.id_actividad, a.nombre
ORDER BY cant_inscripciones DESC
Limit 1;

-- 2. Actividades con cupos disponibles.
SELECT a.id_actividad, a.nombre, (SELECT COUNT(*) FROM inscripciones i WHERE i.id_actividad_deportiva = a.id_actividad AND i.estado = 'confirmada') -- subconslta
FROM actividadesDeportivas a
WHERE a.cupo_max > (SELECT COUNT(*) FROM inscripciones i WHERE i.id_actividad_deportiva = a.id_actividad AND i.estado = 'confirmada');

-- 3. Cantidad de inscriptos por disciplina deportiva.
SELECT COUNT(*) as cant_inscriptos, d.nombre
FROM inscripciones i
JOIN actividadesDeportivas a on i.id_actividad_deportiva = a.id_actividad
JOIN disciplinas d on a.id_disciplina = d.id_disciplina
WHERE i.estado = 'confirmada'
GROUP BY d.nombre;

-- 4.1 Cantidad de inscriptos por carrera
SELECT COUNT(*) cant_inscriptos, c.nombre
FROM inscripciones i
JOIN estudiantes e on i.id_estudiante = e.id_estudiante
JOIN carreras c on e.id_carrera = c.id_carrera
WHERE i.estado = 'confirmada'
GROUP BY c.nombre;

-- 4.2 Cantidad de inscriptos por facultad
SELECT COUNT(*) cant_inscriptos, f.nombre
FROM inscripciones i
JOIN estudiantes e on i.id_estudiante = e.id_estudiante
JOIN carreras c on e.id_carrera = c.id_carrera
JOIN facultades f on c.id_facultad = f.id_facultad
WHERE i.estado = 'confirmada'
GROUP BY f.nombre;