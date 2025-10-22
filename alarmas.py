from db_connection import conectar
from datetime import datetime

def insertar_alarma(hora, fecha, medicamento_id, usuario_id):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        args = [hora, fecha, medicamento_id, usuario_id]
        cur.callproc("sp_insertar_alarma", args)
        cnx.commit()
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_alarmas_hoy(usuario_id):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        cur.callproc("sp_listar_alarmas_hoy", [usuario_id])
        results = []
        for rs in cur.stored_results():
            results.extend(rs.fetchall())
        return results
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def demo(medicamento_id, usuario_id):
    hoy = datetime.now().strftime("%Y-%m-%d")
    insertar_alarma("09:00:00", hoy, medicamento_id, usuario_id)
    alarmas = listar_alarmas_hoy(usuario_id)
    print("Alarmas hoy:", alarmas)