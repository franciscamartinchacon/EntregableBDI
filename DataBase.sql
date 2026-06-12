DROP DATABASE IF EXISTS entregablebd1;
CREATE DATABASE entregablebd1 DEFAULT CHARACTER SET utf8 COLLATE utf8_spanish_ci;
USE entregablebd1;

CREATE TABLE facultades
(
    id_facultad INT AUTO_INCREMENT,
    nombre      VARCHAR(50) NOT NULL UNIQUE,

    PRIMARY KEY (id_facultad)
);

CREATE TABLE carreras
(
    id_carrera  INT AUTO_INCREMENT,
    nombre      VARCHAR(50) NOT NULL,
    id_facultad INT NOT NULL,

    PRIMARY KEY (id_carrera),
    FOREIGN KEY (id_facultad) REFERENCES facultades(id_facultad),
    UNIQUE (nombre, id_facultad)
);

CREATE TABLE estudiantes
(
    id_estudiante INT AUTO_INCREMENT ,
    documento   INT NOT NULL UNIQUE, #unico por cada estudiante
    nombre      VARCHAR(50) NOT NULL,
    apellido    VARCHAR(50) NOT NULL,
    correo      VARCHAR(50) NOT NULL UNIQUE, #unico por cada estudiante
    id_carrera    INT NOT NULL,

    PRIMARY KEY (documento),
    FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);

CREATE TABLE disciplinas
(
    id_disciplina    INT AUTO_INCREMENT,
    nombre           VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (id_disciplina)
);

CREATE TABLE espaciosDeportivos
(
    id_espacio  INT AUTO_INCREMENT,
    nombre      VARCHAR(50) NOT NULL,
    ubicacion   VARCHAR(100) NOT NULL,
    libre       BOOLEAN NOT NULL,

    PRIMARY KEY (id_espacio)
);


CREATE TABLE actividadesDeportivas
(
    id_actividad    INT AUTO_INCREMENT,
    nombre          VARCHAR(50) NOT NULL UNIQUE,
    id_disciplina   INT NOT NULL,
    id_espacio      INT NOT NULL,
    cupo_max        INT NOT NULL,
    dia_semana      ENUM('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'), #unicos valores aceptados
    fecha           DATE NOT NULL,
    horario         TIME NOT NULL,
    estado          ENUM('abierta', 'cerrada', 'finalizada', 'cancelada'), #unicos valores aceptados

    PRIMARY KEY (id_actividad),
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina),
    FOREIGN KEY (id_espacio) REFERENCES espaciosDeportivos(id_espacio),

    CHECK (cupo_max > 0)
);

CREATE TABLE inscripciones
(
    id_inscripcion          INT AUTO_INCREMENT,
    id_estudiante           INT NOT NULL,
    id_actividad_deportiva  INT NOT NULL,
    fecha_inscripcion       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado                  ENUM ('confirmada','lista_espera'),
    PRIMARY KEY (id_estudiante, id_actividad_deportiva,fecha_inscripcion), #controla que un mismo alumno solo se pueda anotar a una misma actividad por dia
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_actividad_deportiva) REFERENCES actividadesDeportivas(id_actividad)
);

CREATE TABLE asistencias
(
    id_asistencia  INT AUTO_INCREMENT,
    id_inscripcion INT NOT NULL,
    fecha          DATE NOT NULL,
    presente       BOOLEAN NOT NULL,

    PRIMARY KEY (id_asistencia),
    FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion),
    UNIQUE (id_inscripcion, fecha)
);

