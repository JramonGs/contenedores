import pytest

from app import Animal, app, db


@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
    )
    with app.app_context():
        db.create_all()

    yield app.test_client()

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_muestra_formulario_para_agregar_animal(client):
    respuesta = client.get('/animales/agregar')

    assert respuesta.status_code == 200
    assert b'name="nombre"' in respuesta.data
    assert b'name="tipo"' in respuesta.data
    assert b'name="edad"' in respuesta.data


def test_agrega_animal_y_redirige_a_la_lista(client):
    respuesta = client.post(
        '/animales/agregar',
        data={'nombre': 'Milo', 'tipo': 'León', 'edad': '5'},
    )

    assert respuesta.status_code == 302
    assert respuesta.headers['Location'] == '/?agregado=1'
    respuesta = client.get(respuesta.headers['Location'])
    assert b'Animal agregado correctamente.' in respuesta.data
    assert b'Milo' in respuesta.data

    with app.app_context():
        animal = db.session.execute(
            db.select(Animal).where(Animal.nombre == 'Milo')
        ).scalar_one()
        assert animal.tipo == 'León'
        assert animal.edad == 5


def test_edad_es_opcional_y_acepta_nombres_de_hasta_cien_caracteres(client):
    nombre = 'N' * 100
    tipo = 'T' * 100
    respuesta = client.post(
        '/animales/agregar',
        data={'nombre': nombre, 'tipo': tipo, 'edad': ''},
    )

    assert respuesta.status_code == 302
    with app.app_context():
        animal = db.session.execute(
            db.select(Animal).where(Animal.nombre == nombre)
        ).scalar_one()
        assert animal.tipo == tipo
        assert animal.edad is None


@pytest.mark.parametrize(
    ('datos', 'mensaje'),
    [
        ({'nombre': '', 'tipo': 'León', 'edad': ''}, 'El nombre es obligatorio.'),
        ({'nombre': 'Milo', 'tipo': '', 'edad': ''}, 'El tipo es obligatorio.'),
        (
            {'nombre': 'Milo', 'tipo': 'León', 'edad': 'años'},
            'La edad debe ser un número entero.',
        ),
        (
            {'nombre': 'Milo', 'tipo': 'León', 'edad': '-1'},
            'La edad no puede ser negativa.',
        ),
        (
            {'nombre': 'N' * 101, 'tipo': 'León', 'edad': ''},
            'El nombre no puede superar los 100 caracteres.',
        ),
        (
            {'nombre': 'Milo', 'tipo': 'T' * 101, 'edad': ''},
            'El tipo no puede superar los 100 caracteres.',
        ),
    ],
)
def test_rechaza_datos_invalidos(client, datos, mensaje):
    respuesta = client.post('/animales/agregar', data=datos)

    assert respuesta.status_code == 400
    assert mensaje.encode() in respuesta.data

    with app.app_context():
        assert db.session.execute(db.select(Animal)).scalars().all() == []
