import os

def init_app(app):
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DB_HOST=os.getenv('DB_HOST'),
        DB_PORT=int(os.getenv('DB_PORT')),
        DB_DATABASE=os.getenv('DB_DATABASE'),
        DB_USERNAME=os.getenv('DB_USERNAME'),
        DB_PASSWORD=os.getenv('DB_PASSWORD'),
    )