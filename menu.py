# Importa el conector oficial de MySQL para Python
import mysql.connector

# ---------- CONFIGURACIÓN DE CONEXIÓN ----------
# Diccionario con los parámetros necesarios para establecer la conexión con la BD.
DB_CONFIG = {
    "host": "localhost",          # Servidor donde corre MySQL (local en este caso)
    "user": "root",               # Usuario con permisos de acceso
    "password": "1234",  # Reemplaza con la contraseña real o déjalo vacío si no tiene
    "database": "empresa"         # Nombre de la base de datos a utilizar
    # "port": 3306,               # (Opcional) solo si tu MySQL usa un puerto distinto
}

# ---------- FUNCIÓN DE CONEXIÓN ----------
def conectar():
    """
    Crea y devuelve una conexión a MySQL usando los parámetros definidos en DB_CONFIG.
    Si la conexión falla, lanzará una excepción de tipo mysql.connector.Error.
    """
    return mysql.connector.connect(**DB_CONFIG)

# ---------- FUNCIONES PRINCIPALES ----------
def sp_insertar(nombre: str, cargo: str, sueldo: float) -> int:
    """
    Inserta un nuevo empleado llamando al procedimiento almacenado:
    sp_insertar_empleado(IN p_nombre, IN p_cargo, IN p_sueldo, OUT p_nuevo_id)
    Devuelve el ID generado por la inserción, o -1 si ocurre un error.
    """
    cnx = cur = None  # Inicializa variables para conexión y cursor
    try:
        cnx = conectar()           # Establece la conexión a la BD
        cur = cnx.cursor()         # Crea un cursor para ejecutar sentencias SQL o SP
        args = [nombre, cargo, sueldo, 0]  # Prepara los argumentos, el último es OUT
        args = cur.callproc("sp_insertar_empleado", args)  # Llama al procedimiento almacenado
        cnx.commit()               # Confirma la transacción (hace persistente la inserción)
        nuevo_id = args[3]         # Recupera el valor OUT (el nuevo ID generado)
        print(f"✅ Insertado correctamente. Nuevo ID: {nuevo_id}")
        return nuevo_id            # Devuelve el ID al programa
    except mysql.connector.Error as e:
        # --- MANEJO DE ERRORES ---
        # Si ocurre un error durante la ejecución del procedimiento (por ejemplo, error de conexión,
        # nombre de SP incorrecto, o violación de restricción en la base de datos),
        # el flujo del programa entra en este bloque 'except'.

        print("❌ Error en sp_insertar:", e)
        # Muestra en pantalla un mensaje de error junto con la descripción técnica
        # que entrega el conector MySQL (contenida en la variable 'e').

        if cnx and cnx.is_connected():
            # Verifica que la conexión a la base de datos exista y siga activa antes de intentar revertir.
            try:
                cnx.rollback()
                # Revierte (anula) cualquier cambio hecho en la transacción actual.
                # Es decir, si se intentó insertar un registro pero falló, no se guardará nada en la BD.
            except:
                pass  # Si fallara el rollback (raro, pero posible), simplemente lo ignora para no detener el programa.

        return -1
        # Devuelve -1 como valor de retorno especial, indicando que la inserción NO se realizó correctamente.
        # Esto permite al programa principal detectar el fallo y actuar en consecuencia (por ejemplo, mostrar un aviso).

        # Cierra los recursos abiertos (cursor y conexión)
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def sp_listar_activos():
    """
    Llama al procedimiento almacenado sp_listar_empleados_activos().
    Muestra en consola todos los registros activos (eliminado = 0).
    """
    cnx = cur = None
    try:
        cnx = conectar()             # Conecta a MySQL
        cur = cnx.cursor()           # Crea un cursor
        cur.callproc("sp_listar_empleados_activos")  # Ejecuta el SP sin parámetros
        print("=== EMPLEADOS ACTIVOS ===")
        # Recupera los resultados devueltos por el SP
        for result in cur.stored_results():
            # Itera sobre cada fila retornada (id, nombre, cargo, sueldo, created_at, updated_at)
            for (id_, nombre, cargo, sueldo, created_at, updated_at) in result.fetchall():
                # Maneja posibles valores NULL en updated_at
                ua = updated_at if updated_at is not None else "-"
                # Imprime los datos formateados
                print(f"ID:{id_:<3} | Nombre:{nombre:<15} | Cargo:{cargo:<13} | "
                f"Sueldo:${sueldo:,.0f} | Creado:{created_at} | Actualizado:{ua}")
    except mysql.connector.Error as e:
        print("❌ Error en sp_listar_activos:", e)
    finally:
        # Cierra recursos abiertos
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def sp_listar_todos():
    """
    Llama al procedimiento almacenado sp_listar_empleados_todos()
    Muestra en consola todos los registros, tanto activos como eliminados.
    """
    cnx = cur = None  # Inicializa las variables para la conexión y el cursor

    try:
        cnx = conectar()               # 1️⃣ Crea la conexión con la base de datos
        cur = cnx.cursor()             # 2️⃣ Crea un cursor para ejecutar sentencias SQL o SP

        cur.callproc("sp_listar_empleados_todos")  # 3️⃣ Llama al procedimiento almacenado
        print("=== EMPLEADOS (TODOS) ===")         # 4️⃣ Imprime un encabezado informativo

        # 5️⃣ 'stored_results()' devuelve un iterador con todos los conjuntos de resultados (result sets)
        # devueltos por el procedimiento almacenado. En este caso, hay solo uno,
        # pero MySQL permite que un SP tenga varios SELECT, y por eso se recorre con 'for'.
        for result in cur.stored_results():

            # 6️⃣ 'fetchall()' obtiene todas las filas del conjunto de resultados.
            # Cada fila llega como una tupla con los valores en el mismo orden del SELECT en el SP:
            # (id, nombre, cargo, sueldo, eliminado, created_at, updated_at, deleted_at)
            for (id_, nombre, cargo, sueldo, eliminado, created_at, updated_at, deleted_at) in result.fetchall():

                # 7️⃣ Determina el estado del empleado según el valor del campo 'eliminado':
                # Si es 0 → ACTIVO, si es 1 → ELIMINADO
                estado = "ACTIVO" if eliminado == 0 else "ELIMINADO"

                # 8️⃣ Maneja posibles valores NULL de la base de datos.
                # MySQL traduce los NULL a 'None' en Python, así que si no hay fecha, muestra un guion.
                ua = updated_at if updated_at is not None else "-"
                da = deleted_at if deleted_at is not None else "-"

                # 9️⃣ Imprime cada fila con formato alineado para que la salida sea legible.
                # - {id_:<3}   → alinea el ID a la izquierda en un ancho de 3 caracteres.
                # - {nombre:<15} → alinea el nombre a la izquierda en un ancho de 15 caracteres.
                # - {cargo:<13} → idem, para el cargo.
                # - {sueldo:,.0f} → formatea el sueldo con separador de miles y sin decimales.
                # - {estado:<9} → deja 9 espacios para el estado (ACTIVO / ELIMINADO).
                # Los demás campos se imprimen tal cual.
                print(
                    f"ID:{id_:<3} | Nombre:{nombre:<15} | Cargo:{cargo:<13} | "
                    f"Sueldo:${sueldo:,.0f} | {estado:<9} | Creado:{created_at} | "
                    f"Actualizado:{ua} | Eliminado:{da}"
                )

    # 10️⃣ Si ocurre un error durante la conexión, ejecución o lectura del SP,
    # este bloque captura la excepción y muestra el detalle del error.
    except mysql.connector.Error as e:
        print("❌ Error en sp_listar_todos:", e)

    # 11️⃣ El bloque 'finally' se ejecuta siempre, haya error o no.
    # Aquí se liberan recursos cerrando el cursor y la conexión correctamente.
    finally:
        if cur:  # Verifica que el cursor exista antes de cerrarlo
            cur.close()
        if cnx and cnx.is_connected():  # Si la conexión está activa, la cierra
            cnx.close()


def sp_borrado_logico(id_empleado: int):
    """
    Marca un empleado como eliminado lógicamente llamando al procedimiento:
    sp_borrado_logico_empleado(IN p_id)
    No borra físicamente el registro, solo cambia el campo 'eliminado' a 1.
    """
    cnx = cur = None  # 1️⃣ Inicializa las variables de conexión (cnx) y cursor (cur) en None.
                    # Esto permite luego verificarlas en el bloque 'finally' aunque ocurra un error.

    try:
        cnx = conectar()      # 2️⃣ Establece la conexión con la base de datos usando la función conectar().
        cur = cnx.cursor()    # 3️⃣ Crea un cursor que permitirá ejecutar sentencias SQL o procedimientos almacenados.

        # 4️⃣ Llama al procedimiento almacenado 'sp_borrado_logico_empleado',
        #     pasándole como parámetro el ID del empleado que se desea marcar como eliminado.
        #     Este procedimiento en la base de datos realiza algo como:
        #     UPDATE empleados SET eliminado = 1, deleted_at = NOW() WHERE id = p_id AND eliminado = 0;
        cur.callproc("sp_borrado_logico_empleado", [id_empleado])

        cnx.commit()          # 5️⃣ Confirma la transacción.
                            #     Esto hace que el cambio (marcar como eliminado) quede guardado definitivamente.
                            #     Si no se llamara a 'commit()', el cambio no se aplicaría en la base de datos.

        # 6️⃣ Informa en consola que el proceso fue exitoso, mostrando el ID afectado.
        print(f"✅ Borrado lógico aplicado al ID {id_empleado} (si estaba activo).")

    # 7️⃣ Captura y maneja cualquier error que ocurra durante el proceso.
    except mysql.connector.Error as e:
        # Muestra un mensaje de error con el detalle que entrega MySQL.
        print("❌ Error en sp_borrado_logico:", e)

        # Si la conexión sigue activa, intenta revertir cualquier cambio no confirmado.
        if cnx and cnx.is_connected():
            try:
                cnx.rollback()  # 8️⃣ Revierte la transacción en caso de fallo.
                                #     Esto asegura que la base de datos no quede en un estado inconsistente.
            except:
                pass            # Si fallara el rollback (raro, pero posible), se ignora para evitar que el programa colapse.

    # 9️⃣ Este bloque se ejecuta siempre, haya ocurrido un error o no.
    finally:
        # Cierra el cursor si existe, liberando el recurso en memoria.
        if cur:
            cur.close()

        # Cierra la conexión con la base de datos si sigue abierta.
        if cnx and cnx.is_connected():
            cnx.close()


def sp_restaurar(id_empleado: int):
    """
    Restaura un empleado eliminado lógicamente llamando a:
    sp_restaurar_empleado(IN p_id)
    Cambia 'eliminado' a 0 y limpia 'deleted_at'.
    """
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        cur.callproc("sp_restaurar_empleado", [id_empleado])
        cnx.commit()
        print(f"✅ Restaurado ID {id_empleado} (si estaba eliminado).")
    except mysql.connector.Error as e:
        print("❌ Error en sp_restaurar:", e)
        if cnx and cnx.is_connected():
            try: cnx.rollback()
            except: pass
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

# ---------------- MENÚ PRINCIPAL ----------------
def menu():
    """
    Muestra un menú interactivo en consola que permite al usuario ejecutar
    las distintas operaciones CRUD a través de los procedimientos almacenados.
    """
    while True:
        # Muestra opciones disponibles
        print("\n===== MENÚ EMPLEADOS (MySQL + SP) =====")
        print("1) Insertar empleado")
        print("2) Listar empleados ACTIVOS")
        print("3) Listar empleados (TODOS)")
        print("4) Borrado lógico por ID")
        print("5) Restaurar por ID (opcional)")
        print("0) Salir")


        # Solicita la opción al usuario
        opcion = input("Selecciona una opción: ").strip()

        # --- Opción 1: Insertar nuevo registro ---
        if opcion == "1":
            nombre = input("Nombre: ").strip()
            cargo  = input("Cargo: ").strip()
            try:
                sueldo = float(input("Sueldo (ej: 750000): ").strip())
            except ValueError:
                print("❌ Sueldo inválido.")
                continue
            sp_insertar(nombre, cargo, sueldo)

        # --- Opción 2: Listar solo empleados activos ---
        elif opcion == "2":
            sp_listar_activos()

        # --- Opción 3: Listar todos los empleados ---
        elif opcion == "3":
            sp_listar_todos()

        # --- Opción 4: Aplicar borrado lógico ---
        elif opcion == "4":
            try:
                id_emp = int(input("ID a eliminar lógicamente: ").strip())
            except ValueError:
                print("❌ ID inválido.")
                continue
            sp_borrado_logico(id_emp)

        # --- Opción 5: Restaurar registro eliminado ---
        elif opcion == "5":
            try:
                id_emp = int(input("ID a restaurar: ").strip())
            except ValueError:
                print("❌ ID inválido.")
                continue
            sp_restaurar(id_emp)

        # --- Opción 0: Salir del menú ---
        elif opcion == "0":
            print("👋 Saliendo del sistema...")
            break

        # --- Opción no válida ---
        else:
            print("❌ Opción no válida. Intenta nuevamente.")

# Punto de entrada del programa
if __name__ == "__main__":
    menu()
