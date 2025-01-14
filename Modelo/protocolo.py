from Modelo.database import conectar_db

class Protocolo:
    def __init__(self, id, titulo, alumno_id, archivo, estado):
        self.id = id
        self.titulo = titulo
        self.alumno_id = alumno_id
        self.archivo = archivo
        self.estado = estado

    @staticmethod
    def obtener_por_id(protocolo_id):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM protocolo WHERE id = ?', (protocolo_id))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return Protocolo(*resultado)
        return None
