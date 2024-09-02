from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from models import db  # Importar db desde models/__init__.py

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configuraciones de la aplicación
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Importar modelos después de inicializar db
from models.empleado import Empleado

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

# Ruta de ejemplo
@app.route('/')
def index():
    return "¡Bienvenido a la API de gestión de empleados!"

# Endpoint para obtener todos los empleados
@app.route('/empleados', methods=['GET'])
def get_empleados():
    empleados = Empleado.query.all()
    return jsonify([empleado.to_dict() for empleado in empleados]), 200

# Endpoint para agregar un nuevo empleado
@app.route('/empleados', methods=['POST'])
def add_empleado():
    nombre = request.form.get('nombre')
    puesto = request.form.get('puesto')
    salario = request.form.get('salario')

    if not nombre or not puesto or not salario:
        return jsonify({'error': 'Datos incompletos'}), 400

    nuevo_empleado = Empleado(
        nombre=nombre,
        puesto=puesto,
        salario=salario
    )

    db.session.add(nuevo_empleado)
    db.session.commit()

    return jsonify(nuevo_empleado.to_dict()), 201
@app.route('/agregar-empleado', methods=['GET'])
def mostrar_formulario():
    return render_template('agregar_empleado.html')
