from db_connection import conectar

def insertar_medicamento(nombre_medicamento, frecuencia, duracion, usuario_id, tratamiento_id):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        args = [nombre_medicamento, frecuencia, duracion, usuario_id, tratamiento_id]
        cur.callproc("sp_insertar_medicamento", args)
        cnx.commit()
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_medicamentos_paciente(usuario_id):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        cur.callproc("sp_listar_medicamentos_paciente", [usuario_id])
        results = []
        for rs in cur.stored_results():
            results.extend(rs.fetchall())
        return results
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def demo(usuario_id):
    insertar_medicamento("DemoMed 10mg", "Cada 12 horas", "7 días", usuario_id, 2)
    meds = listar_medicamentos_paciente(usuario_id)
    print("Medicamentos del usuario:", meds)