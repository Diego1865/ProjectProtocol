import sqlite3
import bcrypt
from Modelo.database import conectar_db

class Usuario:
    def __init__(self, id, correo, nombre, rol):
        self.id = id
        self.correo = correo
        self.nombre = nombre
        self.rol = rol

    @staticmethod
    def validar_login(correo, password):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, correo, nombre, rol, password FROM usuario WHERE correo = ?', (correo,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario[4].encode('utf-8')):
            return Usuario(usuario[0], usuario[1], usuario[2], usuario[3])
        return None
    
    @staticmethod
    def registrar_usuario(matricula, rol, nombre, apellido_paterno, apellido_materno, correo, telefono, password):
        conn = conectar_db()
        cursor = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor.execute('''
                INSERT INTO usuario (matricula, rol, nombre, apellido_paterno, apellido_materno, correo, telefono, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (matricula, rol, nombre, apellido_paterno, apellido_materno, correo, telefono, hashed_password.decode('utf-8')))
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_por_correo(correo):
        conn = conectar_db()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id, correo, nombre, rol FROM usuario WHERE correo = ?', (correo,))
            usuario = cursor.fetchone()
            if usuario:
                return Usuario(usuario[0], usuario[1], usuario[2], usuario[3])  # Ajusta si necesitas más atributos
            return None
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(usuario_id):
        conn = conectar_db()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id, correo, nombre, rol FROM usuario WHERE id = ?', (usuario_id,))
            usuario = cursor.fetchone()
            if usuario:
                return Usuario(usuario[0], usuario[1], usuario[2], usuario[3])  # Ajusta si necesitas más atributos
            return None
        finally:
            conn.close()