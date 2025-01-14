from Modelo.usuario import Usuario
from Modelo.database import conectar_db

class Sinodal(Usuario):
    def __init__(self, id, correo, nombre):
        super().__init__(id, correo, nombre, 'sinodal')

    def evaluar_protocolo(self, protocolo_id, aprobado, razon):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO evaluaciones (protocolo_id, sinodal_id, aprobado, razon)
            VALUES (?, ?, ?, ?)
        ''', (protocolo_id, self.id, aprobado, razon))
        conn.commit()

        # Verificar si todos los sinodales han evaluado
        cursor.execute('SELECT COUNT(*) FROM evaluaciones WHERE protocolo_id = ?', (protocolo_id,))
        total_evaluaciones = cursor.fetchone()[0]

        if total_evaluaciones == 3:
            cursor.execute('SELECT aprobado FROM evaluaciones WHERE protocolo_id = ?', (protocolo_id,))
            resultados = cursor.fetchall()
            if any(not r[0] for r in resultados):
                cursor.execute('UPDATE protocolo SET estado = "Rechazado" WHERE id = ?', (protocolo_id,))
            else:
                cursor.execute('UPDATE protocolo SET estado = "Aprobado" WHERE id = ?', (protocolo_id,))
            conn.commit()

        conn.close()