from flask import Blueprint, redirect, render_template, session, url_for
from Modelo.sinodal import Sinodal

sinodal_bp = Blueprint('sinodal', __name__)

@sinodal_bp.route('/sinodal')
def dashboard():
    if not session.get('logged_in') or session.get('rol') != 'sinodal':
        return redirect(url_for('auth.login'))

    usuario_id = session.get('usuario_id')
    sinodal = Sinodal.obtener_por_id(usuario_id)
    return render_template('Sinodal.html', nombre=sinodal.nombre)