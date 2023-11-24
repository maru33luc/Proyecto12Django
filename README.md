# Clínica de Turnos App

¡Bienvenido a la aplicación de la Clínica de Turnos desarrollada en Django con Python! Esta aplicación te permite gestionar turnos médicos de manera eficiente.

## Requisitos Previos

Antes de comenzar con la configuración y ejecución de la aplicación, asegúrate de tener Python y PostgreSQL instalados en tu sistema.

## Configuración del Entorno Virtual

1. Abre una terminal y navega hasta el directorio raíz de la aplicación.

2. Crea un entorno virtual con el siguiente comando:

   ```bash
   python -m venv venv


3. Activa el entorno virtual con el siguiente comando:

   ```bash
    source venv/bin/activate

4. Instala las dependencias del proyecto con el siguiente comando:

    ```bash
    pip install -r requirements.txt


## Configuración de la Base de Datos

1. Abre una terminal y navega hasta el directorio raíz de la aplicación.

2. Crea una base de datos en PostgreSQL con el siguiente comando:

   ```bash
   createdb clinica_turnos

3. Crea un usuario en PostgreSQL con el siguiente comando:

   ```bash
    createuser -P clinica_turnos

4. Ingresa la contraseña del usuario creado en el paso anterior.

5. Abre el archivo `settings.py` ubicado en `clinica_turnos/settings.py` y modifica las siguientes líneas:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql_psycopg2',
           'NAME': 'clinica_turnos',
           'USER': 'clinica_turnos',
           'PASSWORD': 'password',
           'HOST': 'localhost',
           'PORT': '',
       }
   }

6. Guarda los cambios realizados en el archivo `settings.py`.

7. Ejecuta las migraciones de la base de datos con el siguiente comando:

   ```bash
   python manage.py migrate

## Ejecución de la Aplicación

1. Abre una terminal y navega hasta el directorio raíz de la aplicación
donde se encuentra el archivo `manage.py`( `clinica_turnos/manage.py`).

2. Ejecuta la aplicación con el siguiente comando:

   ```bash
   python manage.py runserver

3. Abre un navegador web y accede a la siguiente URL:

   ```
    http://localhost:8000

## Ejecución de los Tests

1. Abre una terminal y navega hasta el directorio raíz de la aplicación.

2. Ejecuta los tests con el siguiente comando:

   ```bash
   python manage.py test




