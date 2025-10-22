-- =============================================
-- SCRIPT DE INSERCIONES Y CONSULTAS DE PRUEBA
-- Archivo: consultas.sql
-- NOTA: Ejecutar después de 'creacion.sql'
-- =============================================

USE CRONODOSIS;

-- ----------------------------------------------------
-- INSERCIONES DE DATOS REPRESENTATIVOS
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

-- PERSONAS (2 Pacientes y 1 Tutor)
INSERT INTO personas (nombre, correo, rut, telefono, fecha_nacimiento, id_genero, id_alergia, enfermedades_cronicas) VALUES
('Andrea Torres', 'andrea.t@mail.com', '18000111-2', '987654321', '1990-05-15', 1, 3, 'Hipertensión'),
('Juan Perez', 'juan.p@mail.com', '15123456-7', '123456789', '1955-11-20', 2, 2, 'Diabetes Tipo II'),
('Maria Soto (Tutor)', 'maria.s@mail.com', '20123456-k', '998877665', '1985-03-10', 1, 1, NULL);

-- USUARIOS (Asociados a las Personas)
INSERT INTO usuarios (nombre_usuario, password_usuario, id_persona, tipo_usuario_id) VALUES
('andrea_t', 'andrea1234', 1, 1),   -- Paciente (ID 1)
('juan_p', 'juanito55', 2, 1),      -- Paciente (ID 2)
('maria_soto', 'tutor_soto', 3, 2); -- Tutor (ID 3)

-- MEDICAMENTOS (Asociados a los pacientes)
INSERT INTO medicamentos (nombre_medicamento, frecuencia_tratamiento, duracion_tratamiento, usuario_id, id_tratamiento) VALUES
('Losartan 50mg', 'Cada 12 horas', 'Indefinida', 1, 1),      -- Andrea (Crónico)
('Metformina 850mg', 'Cada 8 horas', 'Indefinida', 2, 1),   -- Juan (Crónico)
('Ibuprofeno 400mg', 'Cada 6 horas', '3 días', 1, 2);       -- Andrea (Agudo)

-- ALARMAS (Ejemplo)
INSERT INTO alarmas (hora, fecha, medicamento_id, usuario_id) VALUES
('08:00:00', CURDATE(), 1, 1),
('20:00:00', CURDATE(), 1, 1),
('07:00:00', CURDATE(), 2, 2);

-- HISTORIAL MEDICAMENTOS (Registros de toma)
INSERT INTO historial_medicamentos (medicamento_id, usuario_id, fecha, hora, cumplimiento_tratamiento) VALUES
(1, 1, '2025-10-14', '08:05:00', 'TOMADO'),
(1, 1, '2025-10-14', '20:10:00', 'TOMADO'),
(2, 2, '2025-10-14', '07:30:00', 'NO_TOMADO'), -- Incumplimiento
(3, 1, '2025-10-14', '14:00:00', 'TOMADO');

-- PASTILLEROS
INSERT INTO pastilleros (nombre_pastillero, usuario_id, id_estado) VALUES
('Pastillero Andrea', 1, 1),
('Pastillero Juan', 2, 2);

-- TUTOR_USUARIO (María tutela a Juan)
INSERT INTO tutor_usuario (tutor_id, usuario_id) VALUES
(3, 2);

-- ----------------------------------------------------
-- CONSULTAS DE VERIFICACIÓN Y PRUEBA
-- ----------------------------------------------------

-- 1. Verificar todos los registros de TIPO_USUARIO
SELECT '--- TIPO_USUARIO ---' AS Info, T.* FROM tipo_usuario T;

-- 2. Mostrar todas las PERSONAS ACTIVAS (deleted = 0) con su tipo de género
SELECT 
    P.nombre,
    P.rut,
    G.nombre_genero,
    A.nombre_alergia
FROM personas P
JOIN tipo_genero G ON P.id_genero = G.id_genero
JOIN tipo_alergias A ON P.id_alergia = A.id_alergia
WHERE P.deleted = 0;

-- 3. Listar los MEDICAMENTOS del Paciente Juan Perez (ID 2)
SELECT
    U.nombre_usuario AS Paciente,
    M.nombre_medicamento,
    T.nombre_tratamiento
FROM medicamentos M
JOIN usuarios U ON M.usuario_id = U.id_usuario
JOIN tipo_tratamientos T ON M.id_tratamiento = T.id_tratamiento
WHERE U.id_usuario = 2;

-- 4. Mostrar todas las ALARMAS programadas para el día de hoy
SELECT 
    U.nombre_usuario,
    M.nombre_medicamento,
    A.hora,
    A.fecha
FROM alarmas A
JOIN usuarios U ON A.usuario_id = U.id_usuario
JOIN medicamentos M ON A.medicamento_id = M.id_medicamento
WHERE A.fecha = CURDATE()
ORDER BY A.hora;

-- 5. HISTORIAL: Obtener registros de incumplimiento de tratamiento ('NO_TOMADO')
SELECT
    P.nombre AS Paciente,
    M.nombre_medicamento,
    H.fecha,
    H.hora
FROM historial_medicamentos H
JOIN usuarios U ON H.usuario_id = U.id_usuario
JOIN personas P ON U.id_persona = P.id_persona
JOIN medicamentos M ON H.medicamento_id = M.id_medicamento
WHERE H.cumplimiento_tratamiento = 'NO_TOMADO';

-- 6. Verificar la relación TUTOR-PACIENTE (Quién tutela a quién)
SELECT
    TutorP.nombre AS Nombre_Tutor,
    PacienteP.nombre AS Nombre_Paciente
FROM tutor_usuario TU
JOIN usuarios UT ON TU.tutor_id = UT.id_usuario
JOIN personas TutorP ON UT.id_persona = TutorP.id_persona
JOIN usuarios UU ON TU.usuario_id = UU.id_usuario
JOIN personas PacienteP ON UU.id_persona = PacienteP.id_persona;

-- Agregar consultas de rendimiento
-- 7. Verificar el estado de los pastilleros de todos los usuarios
SELECT 
    P.nombre AS Nombre_Usuario,
    PA.nombre_pastillero,
    EP.nombre_estado
FROM pastilleros PA
JOIN usuarios U ON PA.usuario_id = U.id_usuario
JOIN personas P ON U.id_persona = P.id_persona
JOIN estado_pastillero EP ON PA.id_estado = EP.id_estado
WHERE PA.deleted = 0;

-- 8. Resumen de cumplimiento de tratamientos por usuario
SELECT 
    P.nombre AS Paciente,
    COUNT(CASE WHEN H.cumplimiento_tratamiento = 'TOMADO' THEN 1 END) as Tomados,
    COUNT(CASE WHEN H.cumplimiento_tratamiento = 'NO_TOMADO' THEN 1 END) as No_Tomados
FROM historial_medicamentos H
JOIN usuarios U ON H.usuario_id = U.id_usuario
JOIN personas P ON U.id_persona = P.id_persona
GROUP BY P.nombre;