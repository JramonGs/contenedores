from flask import Blueprint, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


def crear_blueprint(db: SQLAlchemy, modelo_animal: type) -> Blueprint:
    blueprint = Blueprint('animales', __name__)

    @blueprint.route('/animales/agregar', methods=['GET', 'POST'])
    def agregar_animal():
        if request.method == 'GET':
            return render_template('agregar.html', valores={}, errores=[])

        valores = {
            'nombre': request.form.get('nombre', '').strip(),
            'tipo': request.form.get('tipo', '').strip(),
            'edad': request.form.get('edad', '').strip(),
        }
        errores = []

        if not valores['nombre']:
            errores.append('El nombre es obligatorio.')
        elif len(valores['nombre']) > 100:
            errores.append('El nombre no puede superar los 100 caracteres.')
        if not valores['tipo']:
            errores.append('El tipo es obligatorio.')
        elif len(valores['tipo']) > 100:
            errores.append('El tipo no puede superar los 100 caracteres.')

        edad = None
        if valores['edad']:
            try:
                edad = int(valores['edad'])
            except ValueError:
                errores.append('La edad debe ser un número entero.')
            else:
                if edad < 0:
                    errores.append('La edad no puede ser negativa.')

        if errores:
            return render_template(
                'agregar.html',
                valores=valores,
                errores=errores,
            ), 400

        animal = modelo_animal(
            nombre=valores['nombre'],
            tipo=valores['tipo'],
            edad=edad,
        )
        db.session.add(animal)
        db.session.commit()
        return redirect(url_for('index', agregado='1'))

    return blueprint
