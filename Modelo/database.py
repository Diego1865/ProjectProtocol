import sqlite3
import bcrypt

# Conexión a la base de datos
def conectar_db():
    conn = sqlite3.connect('protocolo.db')
    return conn

# Crear la tabla de usuario
def crear_tabla():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            apellido_paterno TEXT NOT NULL,
            apellido_materno TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            telefono TEXT,
            password TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


# Validar el login
def validar_login(matricula, password):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM usuario WHERE matricula = ?', (matricula,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and bcrypt.checkpw(password.encode('utf-8'), resultado[0].encode('utf-8')):
        return True  # Las credenciales son correctas
    return False  # Credenciales incorrectas

def registrar_alumno(matricula, nombre, apellido_paterno, apellido_materno, correo, telefono, password):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        # Encriptar la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insertar el alumno con la contraseña encriptada
        cursor.execute('''
            INSERT INTO usuario (matricula, nombre, apellido_paterno, apellido_materno, correo, telefono, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (matricula, nombre, apellido_paterno, apellido_materno, correo, telefono, hashed_password.decode('utf-8')))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error al registrar el alumno: {e}")
        return False
    finally:
        conn.close()