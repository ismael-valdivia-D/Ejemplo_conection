import mysql.connector
from datetime import datetime

# ---------- CONFIGURACIÓN DE CONEXIÓN ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "CRONODOSIS"
}

def conectar():
    """Establece conexión con la base de datos"""
    return mysql.connector.connect(**DB_CONFIG)

# ---------- FUNCIONES PRINCIPALES ----------
def sp_registrar_paciente():
    """Registra un nuevo paciente con sus datos básicos"""
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        
        # Mostrar géneros disponibles
        cur.execute("SELECT id_genero, nombre_genero FROM tipo_genero WHERE deleted = 0")
        print("\n=== GÉNEROS DISPONIBLES ===")
        for (id_, nombre) in cur.fetchall():
            print(f"{id_}: {nombre}")
            
        # Mostrar alergias disponibles
        cur.execute("SELECT id_alergia, nombre_alergia FROM tipo_alergias WHERE deleted = 0")
        print("\n=== ALERGIAS DISPONIBLES ===")
        for (id_, nombre) in cur.fetchall():
            print(f"{id_}: {nombre}")
            
        # Recopilar datos
        nombre = input("\nNombre completo: ").strip()
        correo = input("Correo electrónico: ").strip()
        rut = input("RUT (XX.XXX.XXX-X): ").strip()
        telefono = input("Teléfono: ").strip()
        fecha_nac = input("Fecha nacimiento (YYYY-MM-DD): ").strip()
        id_genero = int(input("ID del género: "))
        id_alergia = int(input("ID de la alergia: "))
        enf_cronicas = input("Enfermedades crónicas (Enter si no tiene): ").strip() or None
        
        # Insertar persona
        args = [nombre, correo, rut, telefono, fecha_nac, id_genero, id_alergia, enf_cronicas]
        cur.callproc("sp_insertar_persona", args)
        
        # Crear usuario asociado
        usuario = input("Nombre de usuario: ").strip()
        password = input("Contraseña: ").strip()
        
        # Obtener el ID de la persona recién insertada
        cur.execute("SELECT LAST_INSERT_ID()")
        id_persona = cur.fetchone()[0]
        
        # Insertar usuario (tipo 1 = Paciente)
        args = [usuario, password, id_persona, 1]
        cur.callproc("sp_insertar_usuario", args)
        
        cnx.commit()
        print("✅ Paciente registrado correctamente!")
        
    except mysql.connector.Error as e:
        print("❌ Error:", e)
        if cnx and cnx.is_connected():
            cnx.rollback()
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def sp_registrar_medicamento():
    """Registra un nuevo medicamento para un paciente"""
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        
        # Mostrar pacientes disponibles
        cur.execute("""
            SELECT u.id_usuario, p.nombre 
            FROM usuarios u 
            JOIN personas p ON u.id_persona = p.id_persona 
            WHERE u.tipo_usuario_id = 1 AND u.deleted = 0
        """)
        print("\n=== PACIENTES DISPONIBLES ===")
        for (id_, nombre) in cur.fetchall():
            print(f"{id_}: {nombre}")
            
        # Mostrar tipos de tratamiento
        cur.execute("SELECT id_tratamiento, nombre_tratamiento FROM tipo_tratamientos WHERE deleted = 0")
        print("\n=== TIPOS DE TRATAMIENTO ===")
        for (id_, nombre) in cur.fetchall():
            print(f"{id_}: {nombre}")
            
        # Recopilar datos
        usuario_id = int(input("\nID del paciente: "))
        nombre = input("Nombre del medicamento: ").strip()
        frecuencia = input("Frecuencia (ej: Cada 8 horas): ").strip()
        duracion = input("Duración del tratamiento: ").strip()
        tratamiento_id = int(input("ID del tipo de tratamiento: "))
        
        # Insertar medicamento
        args = [nombre, frecuencia, duracion, usuario_id, tratamiento_id]
        cur.callproc("sp_insertar_medicamento", args)
        
        cnx.commit()
        print("✅ Medicamento registrado correctamente!")
        
    except mysql.connector.Error as e:
        print("❌ Error:", e)
        if cnx and cnx.is_connected():
            cnx.rollback()
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def sp_programar_alarma():
    """Programa una nueva alarma para un medicamento"""
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        
        # Mostrar medicamentos activos
        cur.execute("""
            SELECT m.id_medicamento, m.nombre_medicamento, p.nombre
            FROM medicamentos m
            JOIN usuarios u ON m.usuario_id = u.id_usuario
            JOIN personas p ON u.id_persona = p.id_persona
            WHERE m.deleted = 0
        """)
        print("\n=== MEDICAMENTOS DISPONIBLES ===")
        for (id_, med, pac) in cur.fetchall():
            print(f"{id_}: {med} - Paciente: {pac}")
        
        # Recopilar datos
        medicamento_id = int(input("\nID del medicamento: "))
        hora = input("Hora (HH:MM): ").strip()
        fecha = input("Fecha (YYYY-MM-DD) o Enter para hoy: ").strip() or datetime.now().strftime('%Y-%m-%d')
        
        # Obtener usuario_id del medicamento
        cur.execute("SELECT usuario_id FROM medicamentos WHERE id_medicamento = %s", (medicamento_id,))
        usuario_id = cur.fetchone()[0]
        
        # Insertar alarma
        args = [hora, fecha, medicamento_id, usuario_id]
        cur.callproc("sp_insertar_alarma", args)
        
        cnx.commit()
        print("✅ Alarma programada correctamente!")
        
    except mysql.connector.Error as e:
        print("❌ Error:", e)
        if cnx and cnx.is_connected():
            cnx.rollback()
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def sp_registrar_toma():
    """Registra la toma de un medicamento"""
    cnx = cur = None
    
    try:
        
        cnx = conectar()
        cur = cnx.cursor()
        
        # Mostrar medicamentos activos
        cur.execute("""
            SELECT m.id_medicamento, m.nombre_medicamento, p.nombre
            FROM medicamentos m
            JOIN usuarios u ON m.usuario_id = u.id_usuario
            JOIN personas p ON u.id_persona = p.id_persona
            WHERE m.deleted = 0
        """)
        print("\n=== MEDICAMENTOS DISPONIBLES ===")
        for (id_, med, pac) in cur.fetchall():
            print(f"{id_}: {med} - Paciente: {pac}")
        
        # Recopilar datos
        medicamento_id = int(input("\nID del medicamento: "))
        cumplimiento = input("¿Tomado? (TOMADO/NO_TOMADO): ").strip().upper()
        
        if cumplimiento not in ['TOMADO', 'NO_TOMADO']:
            print("❌ Estado inválido. Debe ser TOMADO o NO_TOMADO")
            return
        
        # Obtener usuario_id del medicamento
        cur.execute("SELECT usuario_id FROM medicamentos WHERE id_medicamento = %s", (medicamento_id,))
        usuario_id = cur.fetchone()[0]
        
        # Registrar toma
        args = [medicamento_id, usuario_id, cumplimiento]
        cur.callproc("sp_registrar_toma", args)
        
        cnx.commit()
        print("✅ Toma registrada correctamente!")
        
    except mysql.connector.Error as e:
        print("❌ Error:", e)
        if cnx and cnx.is_connected():
            cnx.rollback()
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def sp_ver_historial():
    """Muestra el historial de tomas de un paciente"""
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        
        # Mostrar pacientes
        cur.execute("""
            SELECT u.id_usuario, p.nombre 
            FROM usuarios u 
            JOIN personas p ON u.id_persona = p.id_persona 
            WHERE u.tipo_usuario_id = 1
        """)
        print("\n=== PACIENTES ===")
        for (id_, nombre) in cur.fetchall():
            print(f"{id_}: {nombre}")
        
        usuario_id = int(input("\nID del paciente: "))
        fecha = input("Fecha a consultar (YYYY-MM-DD) o Enter para hoy: ").strip() or datetime.now().strftime('%Y-%m-%d')
        
        # Llamar al SP y mostrar resultados
        args = [usuario_id, fecha]
        cur.callproc("sp_historial_tomas_paciente", args)
        
        print(f"\n=== HISTORIAL DE TOMAS PARA {fecha} ===")
        for result in cur.stored_results():
            rows = result.fetchall()
            if not rows:
                print("No hay registros para esta fecha")
            for row in rows:
                print(f"\nHora: {row[1]}")
                print(f"Medicamento: {row[2]}")
                print(f"Estado: {row[3]}")
        
    except mysql.connector.Error as e:
        print("❌ Error:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def sp_ver_alarmas_hoy():
    """Muestra las alarmas programadas para hoy"""
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        
        # Mostrar pacientes
        cur.execute("""
            SELECT u.id_usuario, p.nombre 
            FROM usuarios u 
            JOIN personas p ON u.id_persona = p.id_persona 
            WHERE u.tipo_usuario_id = 1
        """)
        print("\n=== PACIENTES ===")
        for (id_, nombre) in cur.fetchall():
            print(f"{id_}: {nombre}")
        
        usuario_id = int(input("\nID del paciente: "))
        
        # Llamar al SP y mostrar resultados
        args = [usuario_id]
        cur.callproc("sp_listar_alarmas_hoy", args)
        
        print("\n=== ALARMAS PARA HOY ===")
        for result in cur.stored_results():
            rows = result.fetchall()
            if not rows:
                print("No hay alarmas programadas para hoy")
            for row in rows:
                print(f"\nHora: {row[0]}")
                print(f"Medicamento: {row[1]}")
                print(f"Frecuencia: {row[2]}")
        
    except mysql.connector.Error as e:
        print("❌ Error:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def sp_ver_medicamentos_paciente():
    """Muestra los medicamentos de un paciente"""
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        
        # Mostrar pacientes
        cur.execute("""
            SELECT u.id_usuario, p.nombre 
            FROM usuarios u 
            JOIN personas p ON u.id_persona = p.id_persona 
            WHERE u.tipo_usuario_id = 1
        """)
        print("\n=== PACIENTES ===")
        for (id_, nombre) in cur.fetchall():
            print(f"{id_}: {nombre}")
        
        usuario_id = int(input("\nID del paciente: "))
        
        # Llamar al SP y mostrar resultados
        args = [usuario_id]
        cur.callproc("sp_listar_medicamentos_paciente", args)
        
        print("\n=== MEDICAMENTOS DEL PACIENTE ===")
        for result in cur.stored_results():
            rows = result.fetchall()
            if not rows:
                print("No hay medicamentos registrados")
            for row in rows:
                print(f"\nMedicamento: {row[0]}")
                print(f"Frecuencia: {row[1]}")
                print(f"Duración: {row[2]}")
                print(f"Tipo: {row[3]}")
        
    except mysql.connector.Error as e:
        print("❌ Error:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def menu():
    """Menú principal del sistema CRONODOSIS"""
    while True:
        print("\n===== SISTEMA CRONODOSIS =====")
        print("1) Registrar nuevo paciente")
        print("2) Registrar medicamento")
        print("3) Programar alarma")
        print("4) Registrar toma de medicamento")
        print("5) Ver historial de tomas")
        print("6) Ver alarmas de hoy")
        print("7) Ver medicamentos de paciente")
        print("0) Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            sp_registrar_paciente()
        elif opcion == "2":
            sp_registrar_medicamento()
        elif opcion == "3":
            sp_programar_alarma()
        elif opcion == "4":
            sp_registrar_toma()
        elif opcion == "5":
            sp_ver_historial()
        elif opcion == "6":
            sp_ver_alarmas_hoy()
        elif opcion == "7":
            sp_ver_medicamentos_paciente()
        elif opcion == "0":
            print("\n👋 ¡Gracias por usar CRONODOSIS!")
            break
        else:
            print("\n❌ Opción no válida")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu()