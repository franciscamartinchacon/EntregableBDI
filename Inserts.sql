USE entregablebd1;

-- Facultades
INSERT INTO facultades (nombre) VALUES
('Facultad de Ingeniería y Tecnologías'),
('Facultad de Ciencias Empresariales'),
('Facultad de Ciencias de la Salud'),
('Facultad de Ciencias Humanas');

-- Carreras
INSERT INTO carreras (nombre, id_facultad) VALUES
('Ingeniería en Informática', 1),
('Ingeniería Industrial', 1),
('Administración de Empresas', 2),
('Contador Público', 2),
('Nutrición', 3),
('Psicología', 4);

-- Estudiantes
INSERT INTO estudiantes (documento, nombre, apellido, correo, id_carrera) VALUES
('55511122', 'Ana', 'Pérez', 'ana.perez@ucu.edu.uy', 1),
('55522233', 'Juan', 'García', 'juan.garcia@ucu.edu.uy', 1),
('55533344', 'Lucía', 'Fernández', 'lucia.fernandez@ucu.edu.uy', 2),
('55544455', 'Mateo', 'Rodríguez', 'mateo.rodriguez@ucu.edu.uy', 3),
('55555566', 'Sofía', 'Martínez', 'sofia.martinez@ucu.edu.uy', 4),
('55566677', 'Valentina', 'Silva', 'valentina.silva@ucu.edu.uy', 5),
('55577788', 'Tomás', 'López', 'tomas.lopez@ucu.edu.uy', 6),
('55588899', 'Martina', 'Sosa', 'martina.sosa@ucu.edu.uy', 1);

-- Disciplinas deportivas
INSERT INTO disciplinas (nombre) VALUES
('Fútbol'),
('Básquetbol'),
('Atletismo'),
('Vóleibol'),
('Yoga'),
('Funcional'),
('Gimnasio');

-- Espacios deportivos
INSERT INTO espaciosDeportivos (nombre, ubicacion) VALUES
('Gimnasio Mullin Tech', 'Edificio Mullin Tech'),
('Sala multiuso Sacré Cœur', 'Edificio Sacré Cœur'),
('Patio deportivo San José', 'Edificio San José'),
('Sala de actividades Lourdes', 'Edificio Lourdes'),
('Espacio recreativo Semprún', 'Edificio Semprún'),
('Sala funcional San Ignacio', 'Edificio San Ignacio');

-- Actividades deportivas
INSERT INTO actividadesDeportivas
(nombre, id_disciplina, id_espacio, cupo_max, dia_semana, fecha, horario, estado)
VALUES
('Fútbol recreativo mixto', 1, 3, 2, 'lunes', '2026-06-10', '18:00:00', 'abierta'),
('Funcional turno mañana', 6, 6, 3, 'martes', '2026-06-11', '08:00:00', 'abierta'),
('Yoga inicial', 5, 2, 2, 'miercoles', '2026-06-12', '19:00:00', 'abierta'),
('Atletismo inicial', 3, 5, 4, 'jueves', '2026-06-13', '17:30:00', 'cerrada'),
('Básquetbol recreativo', 2, 1, 5, 'viernes', '2026-06-14', '18:30:00', 'abierta'),
('Vóleibol mixto', 4, 4, 4, 'sabado', '2026-06-15', '10:00:00', 'cancelada');

-- Inscripciones
INSERT INTO inscripciones
(id_estudiante, id_actividad_deportiva, estado)
VALUES
(1, 1, 'confirmada'),
(2, 1, 'confirmada'),
(3, 1, 'lista_espera'),

(4, 2, 'confirmada'),
(5, 2, 'confirmada'),
(6, 2, 'confirmada'),

(7, 3, 'confirmada'),
(8, 3, 'confirmada'),

(1, 5, 'confirmada'),
(3, 5, 'confirmada'),
(5, 5, 'confirmada');

-- Asistencias
INSERT INTO asistencias
(id_inscripcion, fecha, presente)
VALUES
(1, '2026-06-10', TRUE),
(2, '2026-06-10', FALSE),

(4, '2026-06-11', TRUE),
(5, '2026-06-11', FALSE),
(6, '2026-06-11', TRUE),

(7, '2026-06-12', TRUE),
(8, '2026-06-12', FALSE),

(9, '2026-06-14', TRUE),
(10, '2026-06-14', TRUE),
(11, '2026-06-14', FALSE);