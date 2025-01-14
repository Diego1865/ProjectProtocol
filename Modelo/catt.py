from Modelo.usuario import Usuario
from Modelo.database import conectar_db

class UsuarioCATT(Usuario):
    def __init__(self, id, correo, nombre):
        super().__init__(id, correo, nombre, 'catt')

    def gestionar_usuario(self, usuario_id, accion):
        conn = conectar_db()
        cursor = conn.cursor()

        if accion == 'activar':
            cursor.execute('UPDATE usuario SET activo = 1 WHERE id = ?', (usuario_id,))
        elif accion == 'desactivar':
            cursor.execute('UPDATE usuario SET activo = 0 WHERE id = ?', (usuario_id,))
        
        conn.commit()
        conn.close()