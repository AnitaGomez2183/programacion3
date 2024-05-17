# TeamHub

TeamHub es una aplicación web de mensajería similar a Discord, desarrollada con Flask y MySQL. La finalidad de este proyecto es aprender a integrar conceptos de bases de datos relacionales mediante una aplicación funcional preconfigurada y la base de datos `teamhub` estudiada en la materia de **Programación 3**.

## Requisitos

- Python 3.8 o superior
- MySQL
- Entorno virtual (recomendado)

## Instalación

1. Clona el repositorio:

    ```bash
    git clone repo_url
    cd teamhub_flask
    ```

2. Crea y activa un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno:

    Crea un archivo `.env` en la raíz del proyecto. Adjuntamos un ejemplo de archivo `.env.example`:

    ```bash
    FLASK_APP=run.py
    FLASK_ENV=development
    FLASK_DEBUG=1
    SECRET_KEY=your_secret_key_here
    DB_USER=your_db_user_here
    DB_PASS=your_db_password_here
    DB_HOST=your_db_host_here
    DB_NAME=your_db_name_here
    ```

6. Ejecuta la aplicación:

    ```bash
    flask run
    ```

## Uso

- Accede a `http://127.0.0.1:5000/` en tu navegador para ver la aplicación en funcionamiento.

## Estructura del Proyecto

- `app/` - Contiene el código principal de la aplicación.
- `venv/` - Entorno virtual.
- `run.py` - Punto de entrada para la aplicación.
- `requirements.txt` - Lista de dependencias del proyecto.
- `.env` - Variables de entorno (no se incluye en el control de versiones).

## Contribuciones

Si deseas contribuir al proyecto, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.