from Modelo.usuario import Usuario
from Modelo.database import conectar_db

class Alumno(Usuario):
    def __init__(self, id, nombre, correo, ):
        super().__init__(id, correo, nombre, "alumno")

    def subir_protocolo(self, titulo, archivo_ruta):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO protocolo (titulo, alumno_id, archivo)
            VALUES (?, ?, ?)
        ''', (titulo, self.id, archivo_ruta))
        conn.commit()
        conn.close()



