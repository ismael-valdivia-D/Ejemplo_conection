from db_connection import conectar
from datetime import datetime

def insertar_usuario(nombre_usuario, password, id_persona, tipo_usuario_id=1):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        args = [nombre_usuario, password, id_persona, tipo_usuario_id]
        cur.callproc("sp_insertar_usuario", args)
        cnx.commit()
        cur.execute("SELECT LAST_INSERT_ID()")
        return cur.fetchone()[0]
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def demo_crear_usuario_para_persona(id_persona):
    suf = datetime.now().strftime("%f")[-4:]
    usuario = f"user_demo_{suf}"
    pwd = f"Pwd{ suf }!23"
    uid = insertar_usuario(usuario, pwd, id_persona, 1)
    print("Usuario insertado id:", uid)
    return uid