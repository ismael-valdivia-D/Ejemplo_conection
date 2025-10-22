import os
import mysql.connector

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASS", "1234"),
    "database": os.environ.get("DB_NAME", "CRONODOSIS"),
    "port": int(os.environ.get("DB_PORT", 3306))
}

def conectar():
    """Devuelve una conexión mysql.connector.connect(**DB_CONFIG)"""
    return mysql.connector.connect(**DB_CONFIG)