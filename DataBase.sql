DROP DATABASE IF EXISTS entregablebd1;
CREATE DATABASE entregablebd1 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
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

CREATE TABLE admins
(
    documento INT NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(100) NOT NULL,

    PRIMARY KEY (documento)
);

CREATE TABLE docentes
(
    documento INT NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(100) NOT NULL,

    PRIMARY KEY (documento)
);

CREATE TABLE estudiantes
(
    documento   INT NOT NULL UNIQUE, #unico por cada estudiante
    nombre      VARCHAR(100) NOT NULL,
    apellido    VARCHAR(100) NOT NULL,
    correo      VARCHAR(100) NOT NULL UNIQUE, #unico por cada estudiante
    contrasena  VARCHAR(100) NOT NULL,
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
    dia_semana      ENUM('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo') NOT NULL,
    fecha           DATE NOT NULL,
    hora_inicio     TIME NOT NULL,
    hora_fin        TIME NOT NULL,
    estado          ENUM('abierta', 'cerrada', 'finalizada', 'cancelada') NOT NULL,
    docente_asignado INT NOT NULL,

    PRIMARY KEY (id_actividad),
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina),
    FOREIGN KEY (id_espacio) REFERENCES espaciosDeportivos(id_espacio),
    FOREIGN KEY (docente_asignado) REFERENCES docentes(documento),

    CHECK (cupo_max > 0),
    CHECK (hora_fin > hora_inicio)
);

CREATE TABLE inscripciones
(
    id_inscripcion          INT AUTO_INCREMENT,
    documento               INT NOT NULL,
    id_actividad            INT NOT NULL,
    fecha_inscripcion       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado                  ENUM ('confirmada','lista_espera') NOT NULL,
    PRIMARY KEY (id_inscripcion),
    UNIQUE (documento, id_actividad), #controla que un mismo alumno solo se pueda anotar a una misma actividad por dia
    FOREIGN KEY (documento) REFERENCES estudiantes(documento),
    FOREIGN KEY (id_actividad) REFERENCES actividadesDeportivas(id_actividad)
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


