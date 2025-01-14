import sqlite3

import bcrypt
from Modelo.usuario import Usuario
from Modelo.database import conectar_db

class Alumno(Usuario):
    def __init__(self, id, matricula, nombre, rol, apellido_paterno, apellido_materno, correo, telefono):
        super().__init__(id, correo, nombre, "alumno")
        self.matricula = matricula
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.correo = correo
        self.telefono = telefono


    def subir_protocolo(self, titulo, archivo_ruta):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO protocolo (titulo, alumno_id, archivo)
            VALUES (?, ?, ?)
        ''', (titulo, self.id, archivo_ruta))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_por_id(usuario_id):
        conn = conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT id, matricula, nombre, apellido_paterno, apellido_materno, correo, telefono, rol
                FROM usuario
                WHERE id = ?
            ''', (usuario_id,))
            usuario = cursor.fetchone()

            if usuario:
                # Asegúrate de ajustar el constructor de Alumno según los atributos requeridos
                return Alumno(
                    id=usuario[0],
                    matricula=usuario[1],
                    nombre=usuario[2],
                    apellido_paterno=usuario[3],
                    apellido_materno=usuario[4],
                    correo=usuario[5],
                    telefono=usuario[6],
                    rol=usuario[7]
                )
            return None
        finally:
            conn.close()




