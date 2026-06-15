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

-- Admin
INSERT INTO admins (documento, nombre, apellido, correo, contrasena) VALUES
    (56082008, 'Francisca', 'Martin', 'francisca.martin@ucu.edu.uy', 'admin1'),
    (56258342, 'Sofia', 'Mazzilli', 'sofia.mazzilli@ucu.edu.uy', 'admin2');

-- Docentes
INSERT INTO docentes (documento, nombre, apellido, correo, contrasena) VALUES
(55711122, 'Laura', 'Morales', 'laura.morales@ucu.edu.uy', 'laura123'),
(55722233, 'Diego', 'Castro', 'diego.castro@ucu.edu.uy', 'diego123'),
(55733344, 'Paula', 'Suárez', 'paula.suarez@ucu.edu.uy', 'paula123'),
(55744455, 'Martín', 'Rojas', 'martin.rojas@ucu.edu.uy', 'martin123');

-- Estudiantes
INSERT INTO estudiantes (documento, nombre, apellido, correo, contrasena, id_carrera) VALUES
(55511122, 'Ana', 'Pérez', 'ana.perez@ucu.edu.uy', 'ana123', 1),
(55522233, 'Juan', 'García', 'juan.garcia@ucu.edu.uy', 'juan123', 1),
(55533344, 'Lucía', 'Fernández', 'lucia.fernandez@ucu.edu.uy', 'lucia123', 2),
(55544455, 'Mateo', 'Rodríguez', 'mateo.rodriguez@ucu.edu.uy', 'mateo123', 3),
(55555566, 'Sofía', 'Martínez', 'sofia.martinez@ucu.edu.uy', 'sofia123', 4),
(55566677, 'Valentina', 'Silva', 'valentina.silva@ucu.edu.uy', 'valentina123', 5),
(55577788, 'Tomás', 'López', 'tomas.lopez@ucu.edu.uy', 'tomas123', 6),
(55588899, 'Martina', 'Sosa', 'martina.sosa@ucu.edu.uy', 'martina123', 1),
(55599900, 'Facundo', 'Ramírez', 'facundo.ramirez@ucu.edu.uy', 'facundo123', 2),
(55600011, 'Camila', 'Méndez', 'camila.mendez@ucu.edu.uy', 'camila123', 3);

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
INSERT INTO espaciosDeportivos (nombre, ubicacion, libre) VALUES
('Gimnasio Mullin Tech', 'Edificio Mullin Tech', FALSE),
('Sala multiuso Sacré Cœur', 'Edificio Sacré Cœur', FALSE ),
('Patio deportivo San José', 'Edificio San José', TRUE),
('Sala de actividades Lourdes', 'Edificio Lourdes', TRUE),
('Espacio recreativo Semprún', 'Edificio Semprún', FALSE),
('Sala funcional San Ignacio', 'Edificio San Ignacio', FALSE);

-- Actividades deportivas
INSERT INTO actividadesDeportivas (nombre, id_disciplina, id_espacio, cupo_max, dia_semana, fecha, hora_inicio, hora_fin, estado, docente_asignado) VALUES
('Fútbol recreativo mixto', 1, 3, 2, 'miercoles', '2026-06-10', '18:00:00', '19:00:00', 'abierta', 55711122),
('Funcional turno mañana', 6, 6, 3, 'jueves', '2026-06-11', '08:00:00', '09:00:00', 'abierta', 55722233),
('Yoga inicial', 5, 2, 2, 'viernes', '2026-06-12', '19:00:00', '20:00:00', 'abierta', 55733344),
('Atletismo inicial', 3, 5, 4, 'sabado', '2026-06-13', '17:30:00', '18:30:00', 'cerrada', 55744455),
('Básquetbol recreativo', 2, 1, 5, 'domingo', '2026-06-14', '18:30:00', '20:00:00', 'abierta', 55711122),
('Vóleibol mixto', 4, 4, 4, 'lunes', '2026-06-15', '10:00:00', '11:30:00', 'cancelada', 55722233),
('Gimnasio libre', 7, 1, 6, 'martes', '2026-06-16', '09:00:00', '10:00:00', 'abierta', 55733344);

-- Inscripciones
INSERT INTO inscripciones (documento, id_actividad, estado) VALUES
(55511122, 1, 'confirmada'),
(55522233, 1, 'confirmada'),
(55533344, 1, 'lista_espera'),

(55544455, 2, 'confirmada'),
(55555566, 2, 'confirmada'),
(55566677, 2, 'confirmada'),

(55577788, 3, 'confirmada'),
(55588899, 3, 'confirmada'),

(55511122, 5, 'confirmada'),
(55533344, 5, 'confirmada'),
(55555566, 5, 'confirmada'),

(55577788, 2, 'lista_espera'),
(55600011, 3, 'lista_espera'),

(55522233, 7, 'confirmada'),
(55544455, 7, 'confirmada'),
(55566677, 7, 'confirmada'),
(55599900, 7, 'confirmada');

-- Asistencias
INSERT INTO asistencias (id_inscripcion, fecha, presente) VALUES
(1, '2026-06-10', TRUE),
(2, '2026-06-10', FALSE),
(4, '2026-06-11', TRUE),
(5, '2026-06-11', FALSE),
(6, '2026-06-11', TRUE),
(7, '2026-06-12', TRUE),
(8, '2026-06-12', FALSE),
(9, '2026-06-14', TRUE),
(10, '2026-06-14', TRUE),
(11, '2026-06-14', FALSE),
(14, '2026-06-16', FALSE),
(15, '2026-06-16', TRUE),
(16, '2026-06-16', TRUE),
(17, '2026-06-16', FALSE);