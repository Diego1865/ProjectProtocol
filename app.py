import os
from flask import Flask, send_from_directory
from Control.routes.auth import auth_bp
from Control.routes.alumno import alumno_bp
from Control.routes.protocolo import protocolo_bp
from Control.routes.catt import catt_bp
from Control.routes.sinodal import sinodal_bp

app = Flask(__name__, static_folder='Static')
app.secret_key = "#-$%&/()=?.."
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Ajusta el nombre de la carpeta
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(alumno_bp)
app.register_blueprint(protocolo_bp)
app.register_blueprint(catt_bp)
app.register_blueprint(sinodal_bp)


if __name__ == "__main__":
    app.run(debug=True)
