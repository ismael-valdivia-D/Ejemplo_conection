from db_connection import conectar
from datetime import datetime

def registrar_toma(medicamento_id, usuario_id, cumplimiento):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        args = [medicamento_id, usuario_id, cumplimiento]
        cur.callproc("sp_registrar_toma", args)
        cnx.commit()
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def historial_tomas_paciente(usuario_id, fecha):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        cur.callproc("sp_historial_tomas_paciente", [usuario_id, fecha])
        results = []
        for rs in cur.stored_results():
            results.extend(rs.fetchall())
        return results
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def demo(medicamento_id, usuario_id):
    registrar_toma(medicamento_id, usuario_id, "TOMADO")
    hoy = datetime.now().strftime("%Y-%m-%d")
    rows = historial_tomas_paciente(usuario_id, hoy)
    print("Historial hoy:", rows)