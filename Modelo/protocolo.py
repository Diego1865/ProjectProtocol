from Modelo.database import conectar_db

class Protocolo:
    def __init__(self, id, titulo, alumno_id, archivo, estado):
        self.id = id
        self.titulo = titulo
        self.alumno_id = alumno_id
        self.archivo = archivo
        self.estado = estado

