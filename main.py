import sqlite3
from flask import Flask, request, render_template, redirect, session, url_for
from Modelo import database
from werkzeug.utils import secure_filename
import os

# Crear la aplicación Flask
app = Flask(__name__, static_folder='Static')
app.secret_key = "#-$%&/()=?.."
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Carpeta donde se almacenarán los archivos
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}  # Extensiones permitidas

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ruta principal
@app.route('/')
def index():
    return render_template('Index.html')  # Tu archivo HTML de inicio

# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login_route():
    matricula = request.form['usuario']
    password = request.form['password']

    usuario = database.validar_login(matricula, password)

    if usuario:
        session['logged_in'] = True
        session['usuario'] = matricula  # Guarda información del usuario en la sesión
        return redirect(url_for('alumno')) 
    else:
        mensaje = "Matrícula o contraseña incorrecta."
        return render_template('Index.html', mensaje=mensaje)

@app.route('/alumno')
def alumno():
    if not session.get('logged_in'):
        return redirect(url_for('index'))  # Redirige al inicio de sesión si no está autenticado
    
    matricula = session.get('usuario')
    
    # Consultar la base de datos para obtener el nombre
    conn = sqlite3.connect('protocolo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM usuario WHERE matricula = ?', (matricula,))
    resultado = cursor.fetchone()
    conn.close()

    nombre_usuario = resultado[0] if resultado else "Usuario desconocido"
    return render_template('Alumno.html', nombre=nombre_usuario)

@app.route('/subir_protocolo', methods=['POST'])
def subir_protocolo():
    if 'file' not in request.files:
        return {"success": False, "message": "No se encontró ningún archivo."}, 400

    file = request.files['file']

    if file.filename == '':
        return {"success": False, "message": "No se seleccionó ningún archivo."}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return {"success": True, "message": "Protocolo subido correctamente."}, 200
    else:
        return {"success": False, "message": "Formato de archivo no permitido. Solo se aceptan PDF."}, 400

@app.route('/nuevo_alumno', methods=['GET', 'POST'])
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

        # Registrar el alumno en la base de datos
        exito = database.registrar_alumno(matricula, nombre, apellido_paterno, apellido_materno, correo, telefono, password)
        
        if exito:
            return redirect(url_for('index'))  # Redirige a la página principal tras el registro exitoso
        else:
            mensaje = "Error: Matrícula o correo ya registrados."
            return render_template('Nuevo_alumno.html', mensaje=mensaje)
    return render_template('Nuevo_alumno.html')

@app.route('/logout')
def logout():
    session.clear()  # Limpia toda la información de la sesión
    return redirect(url_for('index'))  # Redirige a la página principal

if __name__ == "__main__":
    database.crear_tabla()
    app.run(debug=True)  # Inicia el servidor
