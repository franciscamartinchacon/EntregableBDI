DROP DATABASE IF EXISTS entregablebd1;
CREATE DATABASE entregablebd1 DEFAULT CHARACTER SET utf8 COLLATE utf8_spanish_ci;
USE entregablebd1;

CREATE TABLE estudiantes
(
    #idEstudiante int auto_increment ???
    docuemnto   VARCHAR(50) NOT NULL UNIQUE, #unico por cada estudiante
    nombre      VARCHAR(50) NOT NULL,
    apellido    VARCHAR(50) NOT NULL,
    correo      VARCHAR(50) NOT NULL UNIQUE, #unico por cada estudiante
    carrera     VARCHAR(50) NOT NULL,
    facultad    VARCHAR(50) NOT NULL,
    PRIMARY KEY (docuemnto)
);

CREATE TABLE disiplinas
(
    idDisiplina    INT AUTO_INCREMENT,
    nombre         VARCHAR(50) NOT NULL,
    PRIMARY KEY (idDisiplina)
);

CREATE TABLE actividadesDeportivas
(
    idActividad     INT AUTO_INCREMENT,
    nombre          VARCHAR(50) NOT NULL,
    id_disiplina    INT NOT NULL,
    id_espacio      VARCHAR(50) NOT NULL,
    cupoMax         INT NOT NULL,
    dia             ENUM('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'), #unicos valores aceptados
    fecha           DATE NOT NULL,
    horario         TIME NOT NULL,
    estado          ENUM('abierta', 'cerrada', 'finalizada', 'cancelada'), #unicos valores aceptados

    PRIMARY KEY (idActividad),
    PRIMARY KEY (nombre),
    FOREIGN KEY (id_disiplina) REFERENCES disiplinas(idDisiplina),
    FOREIGN KEY (id_espacio) REFERENCES espaciosDeportivos(id_espacio)
);

CREATE TABLE espaciosDeportivos
(
    id_espacio  INT AUTO_INCREMENT,
    nombre      VARCHAR(50) ,
    ubicacion   VARCHAR(100),
    libre       BOOLEAN,

    PRIMARY KEY (id_espacio)
);

CREATE TABLE inscripciones
(
    id_inscripcion      INT AUTO_INCREMENT
    #id_estudiante o ci_estudiante foreign key
    #activida_deportiva foreign key
);