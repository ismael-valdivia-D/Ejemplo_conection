from db_connection import conectar
from datetime import datetime

def insertar_persona(nombre, correo, rut, telefono, fecha_nac, id_genero, id_alergia, enf_cronicas):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        args = [nombre, correo, rut, telefono, fecha_nac, id_genero, id_alergia, enf_cronicas]
        cur.callproc("sp_insertar_persona", args)
        cnx.commit()
        # obtener id insertado
        cur.execute("SELECT LAST_INSERT_ID()")
        return cur.fetchone()[0]
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_pacientes_activos():
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor(dictionary=True)
        cur.callproc("sp_listar_pacientes_activos")
        results = []
        for rs in cur.stored_results():
            results.extend(rs.fetchall())
        return results
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def demo():
    suf = datetime.now().strftime("%f")[-4:]
    nombre = f"Demo Persona {suf}"
    correo = f"demo{ suf }@example.com"
    rut = f"99{ suf }-K"
    id_genero = 1
    id_alergia = 1
    pid = insertar_persona(nombre, correo, rut, "600000000", "1990-01-01", id_genero, id_alergia, None)
    print("Persona insertada id:", pid)
    pacientes = listar_pacientes_activos()
    print("Pacientes activos (muestra):", pacientes[:3])