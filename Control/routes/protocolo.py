from flask import Blueprint, current_app, request, session, jsonify
from werkzeug.utils import secure_filename
from Modelo.alumno import Alumno
import os

def allowed_file(filename):
    allowed_extensions = {'pdf'}  # Extensiones permitidas
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

protocolo_bp = Blueprint('protocolo', __name__)

@protocolo_bp.route('/subir_protocolo', methods=['POST'])
def subir_protocolo():
    if not session.get('logged_in') or session.get('rol') != 'alumno':
        return jsonify({"success": False, "message": "No autorizado"}), 403

    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({"success": False, "message": "Archivo no válido"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "Formato no permitido. Solo PDF."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    titulo = filename
    alumno_id = session.get('usuario_id')
    alumno = Alumno.obtener_por_id(alumno_id)
    if not alumno:
        return jsonify({"success": False, "message": "Alumno no encontrado."}), 400

    # Subir protocolo
    try:
        alumno.subir_protocolo(titulo, filepath)
        return jsonify({"success": True, "message": "Protocolo subido correctamente"}), 200
    except Exception as e:
        print(f"Error al subir protocolo: {e}")
        return "Error interno del servidor.", 500
    
