from flask import Blueprint, current_app, jsonify, redirect, render_template, request, send_from_directory, session, url_for
from Modelo.catt import UsuarioCATT
from Modelo.database import conectar_db

catt_bp = Blueprint('catt', __name__)

@catt_bp.route('/catt')
def dashboard():
    if not session.get('logged_in') or session.get('rol') != 'catt':
        return redirect(url_for('auth.login'))

    usuario_id = session.get('usuario_id')
    catt = UsuarioCATT.obtener_por_id(usuario_id)
    return render_template('Catt.html',nombre=catt.nombre)

@catt_bp.route('/uploads/<path:filename>')
def download_file(filename):
    if not session.get('logged_in') or session.get('rol') != 'catt':
        return redirect(url_for('auth.login'))
    
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@catt_bp.route('/validar_protocolos', methods=['GET', 'POST'])
def validar_protocolos():
    if not session.get('logged_in') or session.get('rol') != 'catt':
        return jsonify({"success": False, "message": "No autorizado"}), 403

    conn = conectar_db()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Obtener protocolos en revisión
        cursor.execute('SELECT id, titulo, estado, alumno_id, archivo FROM protocolo WHERE estado = "En revisión"')
        protocolos = cursor.fetchall()
        conn.close()
        
        protocolos = [
        (id, titulo, estado, alumno_id, archivo.replace('\\', '/'))
        for id, titulo, estado, alumno_id, archivo in protocolos
        ]
        
        return jsonify(protocolos)

    if request.method == 'POST':
        data = request.get_json()
        protocolo_id = data.get('protocolo_id')
        accion = data.get('accion')

        if accion == 'Validar':
            nuevo_titulo = data.get('nuevo_titulo')
            academia = data.get('academia')
            cursor.execute('''
                UPDATE protocolo
                SET titulo = ?, academia = ?, estado = "Validado"
                WHERE id = ?
            ''', (nuevo_titulo, academia, protocolo_id))

        elif accion == 'Rechazar':
            razon = request.form.get('razon_rechazo')

            cursor.execute('''
                UPDATE protocolo
                SET estado = "Rechazado", titulo = titulo || " - Rechazado"
                WHERE id = ?
            ''', (protocolo_id,))
            
            # Guardar la razón del rechazo (agregar una tabla para historiales si es necesario)
            cursor.execute('''
                INSERT INTO historial_rechazos (protocolo_id, razon)
                VALUES (?, ?)
            ''', (protocolo_id, razon))
        
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": f"Protocolo {accion} correctamente"})