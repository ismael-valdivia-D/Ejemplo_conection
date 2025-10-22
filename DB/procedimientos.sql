USE CRONODOSIS;

DELIMITER //

-- Procedimientos para PERSONAS
CREATE PROCEDURE sp_insertar_persona(
    IN p_nombre VARCHAR(100),
    IN p_correo VARCHAR(100),
    IN p_rut VARCHAR(20),
    IN p_telefono VARCHAR(15),
    IN p_fecha_nacimiento DATE,
    IN p_id_genero INT,
    IN p_id_alergia INT,
    IN p_enfermedades_cronicas VARCHAR(200)
)
BEGIN
    INSERT INTO personas(
        nombre, correo, rut, telefono, 
        fecha_nacimiento, id_genero, id_alergia, 
        enfermedades_cronicas
    ) VALUES (
        p_nombre, p_correo, p_rut, p_telefono,
        p_fecha_nacimiento, p_id_genero, p_id_alergia,
        p_enfermedades_cronicas
    );
END //

-- Procedimientos para USUARIOS
CREATE PROCEDURE sp_insertar_usuario(
    IN p_nombre_usuario VARCHAR(45),
    IN p_password_usuario VARCHAR(100),
    IN p_id_persona INT,
    IN p_tipo_usuario_id INT
)
BEGIN
    INSERT INTO usuarios(
        nombre_usuario, password_usuario,
        id_persona, tipo_usuario_id
    ) VALUES (
        p_nombre_usuario, p_password_usuario,
        p_id_persona, p_tipo_usuario_id
    );
END //

-- Procedimientos para MEDICAMENTOS
CREATE PROCEDURE sp_insertar_medicamento(
    IN p_nombre_medicamento VARCHAR(100),
    IN p_frecuencia VARCHAR(50),
    IN p_duracion VARCHAR(100),
    IN p_usuario_id INT,
    IN p_tratamiento_id INT
)
BEGIN
    INSERT INTO medicamentos(
        nombre_medicamento, frecuencia_tratamiento,
        duracion_tratamiento, usuario_id, id_tratamiento
    ) VALUES (
        p_nombre_medicamento, p_frecuencia,
        p_duracion, p_usuario_id, p_tratamiento_id
    );
END //

-- Procedimientos para ALARMAS
CREATE PROCEDURE sp_insertar_alarma(
    IN p_hora TIME,
    IN p_fecha DATE,
    IN p_medicamento_id INT,
    IN p_usuario_id INT
)
BEGIN
    INSERT INTO alarmas(
        hora, fecha, medicamento_id, usuario_id
    ) VALUES (
        p_hora, p_fecha, p_medicamento_id, p_usuario_id
    );
END //

-- Procedimientos de CONSULTA
CREATE PROCEDURE sp_listar_pacientes_activos()
BEGIN
    SELECT 
        p.id_persona,
        p.nombre,
        p.correo,
        p.rut,
        p.telefono,
        p.fecha_nacimiento,
        g.nombre_genero,
        a.nombre_alergia,
        p.enfermedades_cronicas
    FROM personas p
    JOIN usuarios u ON p.id_persona = u.id_persona
    JOIN tipo_genero g ON p.id_genero = g.id_genero
    JOIN tipo_alergias a ON p.id_alergia = a.id_alergia
    WHERE p.deleted = 0 
    AND u.tipo_usuario_id = 1;
END //

CREATE PROCEDURE sp_listar_medicamentos_paciente(
    IN p_usuario_id INT
)
BEGIN
    SELECT 
        m.nombre_medicamento,
        m.frecuencia_tratamiento,
        m.duracion_tratamiento,
        t.nombre_tratamiento
    FROM medicamentos m
    JOIN tipo_tratamientos t ON m.id_tratamiento = t.id_tratamiento
    WHERE m.usuario_id = p_usuario_id
    AND m.deleted = 0;
END //

CREATE PROCEDURE sp_listar_alarmas_hoy(
    IN p_usuario_id INT
)
BEGIN
    SELECT 
        a.hora,
        m.nombre_medicamento,
        m.frecuencia_tratamiento
    FROM alarmas a
    JOIN medicamentos m ON a.medicamento_id = m.id_medicamento
    WHERE a.fecha = CURDATE()
    AND a.usuario_id = p_usuario_id
    AND a.deleted = 0
    ORDER BY a.hora;
END //

CREATE PROCEDURE sp_registrar_toma(
    IN p_medicamento_id INT,
    IN p_usuario_id INT,
    IN p_cumplimiento ENUM('TOMADO', 'NO_TOMADO')
)
BEGIN
    INSERT INTO historial_medicamentos(
        medicamento_id, usuario_id,
        fecha, hora, cumplimiento_tratamiento
    ) VALUES (
        p_medicamento_id, p_usuario_id,
        CURDATE(), CURTIME(), p_cumplimiento
    );
END //

CREATE PROCEDURE sp_historial_tomas_paciente(
    IN p_usuario_id INT,
    IN p_fecha DATE
)
BEGIN
    SELECT 
        h.fecha,
        h.hora,
        m.nombre_medicamento,
        h.cumplimiento_tratamiento
    FROM historial_medicamentos h
    JOIN medicamentos m ON h.medicamento_id = m.id_medicamento
    WHERE h.usuario_id = p_usuario_id
    AND h.fecha = p_fecha
    AND h.deleted = 0
    ORDER BY h.hora DESC;
END //

DELIMITER ;

-- Ejemplo de uso:
/*
CALL sp_insertar_persona('Juan Pérez', 'juan@email.com', '12345678-9', '912345678', '1990-01-01', 1, 1, 'Ninguna');
CALL sp_listar_pacientes_activos();
CALL sp_listar_medicamentos_paciente(1);
CALL sp_listar_alarmas_hoy(1);
CALL sp_registrar_toma(1, 1, 'TOMADO');
CALL sp_historial_tomas_paciente(1, CURDATE());
*/