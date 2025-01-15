from flask import Blueprint, redirect, render_template, session, url_for
from Modelo.catt import UsuarioCATT

catt_bp = Blueprint('catt', __name__)

@catt_bp.route('/catt')
def dashboard():
    if not session.get('logged_in') or session.get('rol') != 'catt':
        return redirect(url_for('auth.login'))

    usuario_id = session.get('usuario_id')
    catt = UsuarioCATT.obtener_por_id(usuario_id)
    return render_template('Catt.html',nombre=catt.nombre)