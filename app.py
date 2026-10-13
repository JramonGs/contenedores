from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. Primero las configuraciones
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zoo_dev_op@host.docker.internal:3306/zoo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Después inicializas la base de datos
db = SQLAlchemy(app)

# 3. Definimos el modelo de datos.
class Animal(db.Model):
    __tablename__ = 'animales'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer)

@app.route('/')
def index():
    
    # Consultamos todos los animales de la base de datos
    lista_animales = Animal.query.all()
    
    # Renderizamos la plantilla index.html y pasamos la lista de animales.
    return render_template('index.html', animales=lista_animales)

if __name__ == '__main__':
    # Agregamos host='0.0.0.0' para que Flask sea accesible desde fuera del contenedor de desarrollo
    app.run(host='0.0.0.0', port=5000)