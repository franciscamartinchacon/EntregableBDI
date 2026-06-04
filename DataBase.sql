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
    id_estudiante int auto_increment,
    documento   VARCHAR(50) NOT NULL UNIQUE, #unico por cada estudiante
    nombre      VARCHAR(50) NOT NULL,
    apellido    VARCHAR(50) NOT NULL,
    correo      VARCHAR(50) NOT NULL UNIQUE, #unico por cada estudiante
    carrera     VARCHAR(50) NOT NULL,
    facultad    VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_estudiante)
);

CREATE TABLE disciplinas
(
    id_disciplina    INT AUTO_INCREMENT,
    nombre         VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_disciplina)
);

CREATE TABLE espaciosDeportivos
(
    id_espacio  INT AUTO_INCREMENT,
    nombre      VARCHAR(50) ,
    ubicacion   VARCHAR(100),
    libre       BOOLEAN,

    PRIMARY KEY (id_espacio)
);


CREATE TABLE actividadesDeportivas
(
    id_actividad    INT AUTO_INCREMENT,
    nombre          VARCHAR(50) NOT NULL,
    id_disciplina   INT NOT NULL,
    id_espacio      INT NOT NULL,
    cupo_max        INT NOT NULL,
    dia_semana      ENUM('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'), #unicos valores aceptados
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
    id_estudiante           INT, #evaluar unique
    id_actividad_deportiva  INT,
    fecha_inscripcion        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado                  ENUM ('confirmada','lista_espera','cancelada'),
    PRIMARY KEY (id_inscripcion),
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_actividad_deportiva) REFERENCES actividadesDeportivas(id_actividad),

    UNIQUE (id_estudiante, id_actividad_deportiva)  #ver consigna
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