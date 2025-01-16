import sqlite3
import os

def conectar_db():
    conn = sqlite3.connect('protocolo.db')
    return conn

def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS "usuario" (
                "id"	INTEGER,
                "matricula"	TEXT NOT NULL UNIQUE,
                "rol"	TEXT NOT NULL,
                "nombre"	TEXT NOT NULL,
                "apellido_paterno"	TEXT NOT NULL,
                "apellido_materno"	TEXT NOT NULL,
                "correo"	TEXT NOT NULL UNIQUE,
                "telefono"	TEXT,
                "password"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        ''')
    conn.commit()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS "protocolo" (
                "id"	INTEGER,
                "titulo"	TEXT NOT NULL,
                "estado"	TEXT NOT NULL default 'En revisión',
                "sinodal"	TEXT,
                "fecha"	TEXT NOT NULL default CURRENT_TIMESTAMP,
                "archivo"	TEXT NOT NULL,
                "academia"	TEXT,
                "alumno_id"	INTEGER NOT NULL,
                FOREIGN KEY("alumno_id") REFERENCES "usuario"("id"),
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "historial_rechazos" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "protocolo_id" INTEGER NOT NULL,
            "razon" TEXT NOT NULL,
            FOREIGN KEY("protocolo_id") REFERENCES "protocolo"("id")
        );
    ''')
    cursor = conn.cursor()
    conn.commit()
    
    conn.close()
    print("Rutas actualizadas con éxito.")
    
    conn.close()

if __name__ == "__main__":
    if not os.path.exists('protocolo.db'):
        crear_tablas()
        print("Base de datos creada.")
    else:
        print("La base de datos ya existe.")