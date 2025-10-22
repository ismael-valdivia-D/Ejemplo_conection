-- =============================================
-- SCRIPT COMPLETO DE LA BASE DE DATOS CRONODOSIS
-- Incluye:
-- 1. Creación de la base de datos
-- 2. Creación de tablas
-- 3. Procedimientos almacenados
-- 4. Datos de prueba
-- =============================================

SET FOREIGN_KEY_CHECKS = 0;
DROP DATABASE IF EXISTS CRONODOSIS;
CREATE DATABASE IF NOT EXISTS CRONODOSIS;
USE CRONODOSIS;

-- ----------------------------------------------------
-- CREACIÓN DE TABLAS
-- ----------------------------------------------------

-- TABLA: TIPO DE GENERO
CREATE TABLE tipo_genero (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    nombre_genero VARCHAR(20) NOT NULL UNIQUE CHECK (CHAR_LENGTH(nombre_genero) >= 2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE
);

-- TABLA: TIPO DE ALERGIAS
CREATE TABLE tipo_alergias (
    id_alergia INT AUTO_INCREMENT PRIMARY KEY,
    nombre_alergia VARCHAR(100) NOT NULL UNIQUE CHECK (CHAR_LENGTH(nombre_alergia) >= 3),
    descripcion VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE
);

-- TABLA: TIPO DE USUARIO
CREATE TABLE tipo_usuario (
    id_tipo_u INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo_u VARCHAR(50) NOT NULL UNIQUE CHECK (CHAR_LENGTH(nombre_tipo_u) >= 3),
    descripcion_tipo_u VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE
);

-- TABLA: TIPO TRATAMIENTOS
CREATE TABLE tipo_tratamientos (
    id_tratamiento INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tratamiento VARCHAR(100) NOT NULL UNIQUE CHECK (CHAR_LENGTH(nombre_tratamiento) >= 3),
    descripcion VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE
);

-- TABLA: ESTADO PASTILLERO
CREATE TABLE estado_pastillero (
    id_estado INT AUTO_INCREMENT PRIMARY KEY,
    nombre_estado VARCHAR(50) NOT NULL UNIQUE CHECK (CHAR_LENGTH(nombre_estado) >= 3),
    descripcion VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE
);

-- TABLA: PERSONAS
CREATE TABLE personas (
    id_persona INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL CHECK (CHAR_LENGTH(nombre) >= 3),
    correo VARCHAR(100) UNIQUE CHECK (correo LIKE '%@%.%'),
    rut VARCHAR(20) NOT NULL UNIQUE CHECK (CHAR_LENGTH(rut) >= 8),
    telefono VARCHAR(15) CHECK (CHAR_LENGTH(telefono) >= 8),
    fecha_nacimiento DATE,
    id_genero INT,
    id_alergia INT,
    enfermedades_cronicas VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_genero) REFERENCES tipo_genero(id_genero),
    FOREIGN KEY (id_alergia) REFERENCES tipo_alergias(id_alergia)
);

-- TABLA: USUARIOS
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(45) NOT NULL CHECK (CHAR_LENGTH(nombre_usuario) >= 3),
    password_usuario VARCHAR(100) NOT NULL CHECK (CHAR_LENGTH(password_usuario) >= 8),
    id_persona INT NOT NULL,
    tipo_usuario_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_persona) REFERENCES personas(id_persona),
    FOREIGN KEY (tipo_usuario_id) REFERENCES tipo_usuario(id_tipo_u)
);

-- TABLA: MEDICAMENTOS
CREATE TABLE medicamentos (
    id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre_medicamento VARCHAR(100) NOT NULL CHECK (CHAR_LENGTH(nombre_medicamento) >= 3),
    frecuencia_tratamiento VARCHAR(50) NOT NULL CHECK (CHAR_LENGTH(frecuencia_tratamiento) >= 1),
    duracion_tratamiento VARCHAR(100) NOT NULL CHECK (CHAR_LENGTH(duracion_tratamiento) >= 1),
    usuario_id INT NOT NULL,
    id_tratamiento INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_tratamiento) REFERENCES tipo_tratamientos(id_tratamiento)
);

-- TABLA: ALARMAS
CREATE TABLE alarmas (
    id_alarma INT AUTO_INCREMENT PRIMARY KEY,
    hora TIME NOT NULL,
    fecha DATE NOT NULL,
    medicamento_id INT NOT NULL,
    usuario_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id_medicamento),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
);

-- TABLA: HISTORIAL MEDICAMENTOS
CREATE TABLE historial_medicamentos (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    medicamento_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    cumplimiento_tratamiento ENUM('TOMADO', 'NO_TOMADO') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id_medicamento),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
);

-- TABLA: PASTILLEROS
CREATE TABLE pastilleros (
    id_pastillero INT AUTO_INCREMENT PRIMARY KEY,
    nombre_pastillero VARCHAR(100) NOT NULL CHECK (CHAR_LENGTH(nombre_pastillero) >= 3),
    usuario_id INT NOT NULL UNIQUE,
    id_estado INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_estado) REFERENCES estado_pastillero(id_estado)
);

-- TABLA: RELACION TUTOR-USUARIO
CREATE TABLE tutor_usuario (
    id_tutor_usuario INT AUTO_INCREMENT PRIMARY KEY,
    tutor_id INT NOT NULL,
    usuario_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    updated_by INT,
    deleted BOOLEAN DEFAULT FALSE,
    UNIQUE (tutor_id, usuario_id),
    CHECK (tutor_id <> usuario_id),
    FOREIGN KEY (tutor_id) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
);

-- Agregar índices para mejorar el rendimiento
CREATE INDEX idx_personas_rut ON personas(rut);
CREATE INDEX idx_usuarios_nombre ON usuarios(nombre_usuario);
CREATE INDEX idx_medicamentos_usuario ON medicamentos(usuario_id);
CREATE INDEX idx_alarmas_fecha ON alarmas(fecha);
CREATE INDEX idx_historial_fecha ON historial_medicamentos(fecha);

-- ----------------------------------------------------
-- PROCEDIMIENTOS ALMACENADOS
-- ----------------------------------------------------

DELIMITER //

-- ... [Aquí van todos los procedimientos almacenados del archivo procedimientos.sql] ...

-- ----------------------------------------------------
-- DATOS DE PRUEBA
-- ----------------------------------------------------

-- TIPO_GENERO
INSERT INTO tipo_genero (nombre_genero) VALUES
('Femenino'), ('Masculino'), ('Otro');

-- TIPO_ALERGIAS
INSERT INTO tipo_alergias (nombre_alergia, descripcion) VALUES
('Sin Alergias', 'El usuario no presenta alergias conocidas.'),
('Alergia a la Penicilina', 'Reacción alérgica a antibióticos de la familia Penicilina.'),
('Alergia a AINEs', 'Reacción a Antiinflamatorios No Esteroideos.');

-- TIPO_USUARIO
INSERT INTO tipo_usuario (nombre_tipo_u, descripcion_tipo_u) VALUES
('Paciente', 'Usuario principal que gestiona su medicación.'),
('Tutor', 'Usuario con permiso para monitorizar a un Paciente.');

-- TIPO_TRATAMIENTOS
INSERT INTO tipo_tratamientos (nombre_tratamiento, descripcion) VALUES
('Crónico', 'Tratamiento de larga duración o indefinido.'),
('Agudo', 'Tratamiento de corta duración, como antibióticos.');

-- ESTADO_PASTILLERO
INSERT INTO estado_pastillero (nombre_estado, descripcion) VALUES
('Conectado', 'Dispositivo pastillero activo y en línea.'),
('Desconectado', 'Dispositivo pastillero inactivo o sin conexión.');

-- PERSONAS
INSERT INTO personas (nombre, correo, rut, telefono, fecha_nacimiento, id_genero, id_alergia, enfermedades_cronicas) VALUES
('Andrea Torres', 'andrea.t@mail.com', '18000111-2', '987654321', '1990-05-15', 1, 3, 'Hipertensión'),
('Juan Perez', 'juan.p@mail.com', '15123456-7', '123456789', '1955-11-20', 2, 2, 'Diabetes Tipo II'),
('Maria Soto (Tutor)', 'maria.s@mail.com', '20123456-k', '998877665', '1985-03-10', 1, 1, NULL);

-- USUARIOS
INSERT INTO usuarios (nombre_usuario, password_usuario, id_persona, tipo_usuario_id) VALUES
('andrea_t', 'andrea1234', 1, 1),
('juan_p', 'juanito55', 2, 1),
('maria_soto', 'tutor_soto', 3, 2);

-- MEDICAMENTOS
INSERT INTO medicamentos (nombre_medicamento, frecuencia_tratamiento, duracion_tratamiento, usuario_id, id_tratamiento) VALUES
('Losartan 50mg', 'Cada 12 horas', 'Indefinida', 1, 1),
('Metformina 850mg', 'Cada 8 horas', 'Indefinida', 2, 1),
('Ibuprofeno 400mg', 'Cada 6 horas', '3 días', 1, 2);

-- ALARMAS
INSERT INTO alarmas (hora, fecha, medicamento_id, usuario_id) VALUES
('08:00:00', CURDATE(), 1, 1),
('20:00:00', CURDATE(), 1, 1),
('07:00:00', CURDATE(), 2, 2);

-- HISTORIAL MEDICAMENTOS
INSERT INTO historial_medicamentos (medicamento_id, usuario_id, fecha, hora, cumplimiento_tratamiento) VALUES
(1, 1, CURDATE(), '08:05:00', 'TOMADO'),
(1, 1, CURDATE(), '20:10:00', 'TOMADO'),
(2, 2, CURDATE(), '07:30:00', 'NO_TOMADO'),
(3, 1, CURDATE(), '14:00:00', 'TOMADO');

-- PASTILLEROS
INSERT INTO pastilleros (nombre_pastillero, usuario_id, id_estado) VALUES
('Pastillero Andrea', 1, 1),
('Pastillero Juan', 2, 2);

-- TUTOR_USUARIO
INSERT INTO tutor_usuario (tutor_id, usuario_id) VALUES
(3, 2);

SET FOREIGN_KEY_CHECKS = 1;

-- Fin del script