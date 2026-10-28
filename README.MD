# Proyecto ZOO
Este proyecto sirve para administrar un **ZOOLOGICO**

## Instalacion
Para ejecutar este proyecto instala las dependecias del archivo requiremente.txt utilizando el siguiente comando:

pip install -r requirements.txt

## Saludo
Practica de dependencias y contenedores.

## Agregar animales
Desde la lista, selecciona **Agregar animal** y completa el nombre y el tipo.
La edad es opcional, pero si se indica debe ser un número entero no negativo.

## Red Docker compartida
La aplicación usa `db_proyecto_zoo` como host de MySQL. El contenedor de
desarrollo y el contenedor de base de datos deben estar en la red
`zoo_network`.

Ejecuta estos comandos desde una terminal del sistema anfitrión:

```bash
docker network create zoo_network
docker network connect zoo_network db_proyecto_zoo
```

Si la red ya existe, el primer comando puede mostrar un error; en ese caso
continúa con el segundo. Después reconstruye o vuelve a abrir el contenedor de
desarrollo en VS Code.

Dentro del contenedor de desarrollo, verifica la conexión:

```bash
getent hosts db_proyecto_zoo
python -c "import socket; socket.create_connection(('db_proyecto_zoo', 3306), timeout=5); print('MySQL accesible')"
```

Inicia Flask con:

```bash
python app.py
```

Al iniciar, la aplicación crea automáticamente las tablas definidas que aún no
existan, incluida `animales`.

La aplicación estará disponible en `http://localhost:5000`.