from flask import Blueprint, request, session, redirect, url_for, render_template
from Modelo.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('Index.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    password = request.form['password']

    usuario = Usuario.validar_login(correo, password)

    if usuario:
        session['logged_in'] = True
        session['usuario_id'] = usuario.id
        session['rol'] = usuario.rol

        if usuario.rol == 'alumno':
            return redirect(url_for('alumno.dashboard'))
        elif usuario.rol == 'sinodal':
            return redirect(url_for('sinodal.dashboard'))
        elif usuario.rol == 'catt':
            return redirect(url_for('catt.dashboard'))
    else:
        mensaje = "Correo o contraseña incorrectos."
        return render_template('Index.html', mensaje=mensaje)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))
