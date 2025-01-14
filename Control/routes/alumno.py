from flask import Blueprint, request, session, redirect, url_for, render_template
from Modelo.alumno import Alumno
from Modelo.usuario import Usuario

alumno_bp = Blueprint('alumno', __name__)

@alumno_bp.route('/alumno')
def dashboard():
    if not session.get('logged_in') or session.get('rol') != 'alumno':
        return redirect(url_for('auth.login'))

    usuario_id = session.get('usuario_id')
    alumno = Alumno.obtener_por_id(usuario_id)
    return render_template('Alumno.html', nombre=alumno.nombre)

@alumno_bp.route('/nuevo_alumno', methods=['GET', 'POST'])
def nuevo_alumno():
    if request.method == 'POST':
        # Obtener datos del formulario
        matricula = request.form['matricula']
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellidoPaterno']
        apellido_materno = request.form['apellidoMaterno']
        correo = request.form['correo']
        telefono = request.form['telefono']
        password = request.form['contraseña']
        rol = 'alumno'

        # Registrar el alumno en la base de datos
        exito = Usuario.registrar_usuario(matricula, rol, nombre, apellido_paterno, apellido_materno, correo, telefono, password)
        
        if exito:
            return redirect(url_for('auth.index'))  # Redirige a la página principal tras el registro exitoso
        else:
            mensaje = "Error: Matrícula o correo ya registrados."
            return render_template('Nuevo_alumno.html', mensaje=mensaje)
    return render_template('Nuevo_alumno.html')