import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from animales.agregar import crear_blueprint

load_dotenv()

app = Flask(__name__)

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT', '3306')
db_name = os.environ.get('DB_NAME')

if not all((db_user, db_password, db_host, db_name)):
    raise RuntimeError(
        'Faltan variables de conexión: DB_USER, DB_PASSWORD, DB_HOST y DB_NAME.'
    )

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{quote_plus(db_user)}:{quote_plus(db_password)}'
    f'@{db_host}:{db_port}/{quote_plus(db_name)}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Animal(db.Model):
    __tablename__ = 'animales'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer)


app.register_blueprint(crear_blueprint(db, Animal))


def inicializar_base_de_datos():
    with app.app_context():
        db.create_all()


@app.route('/')
def index():
    lista_animales = Animal.query.all()
    return render_template(
        'index.html',
        animales=lista_animales,
        agregado=request.args.get('agregado') == '1',
    )


if __name__ == '__main__':
    inicializar_base_de_datos()
    app.run(host='0.0.0.0', port=5000)
