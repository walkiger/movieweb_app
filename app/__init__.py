from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database and create the database file if it doesn't exist.

    :param app: The Flask application instance
    """
    db_path = os.path.join(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_path):
        os.makedirs(db_dir, exist_ok=True)  # Ensure the directory exists
        with app.app_context():
            db.create_all()
            print('Database file created successfully')

def create_app():
    """
    Factory function to create and configure the Flask application.

    :return: Configured Flask application instance.
    """
    app = Flask(__name__, static_folder='../static')  # Set the static folder
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # Import models and data manager
        from .data_manager.sqlite_data_manager import User, Movie, SQLiteDataManager
        init_db(app)  # Ensure database file is created if it doesn't exist
        app.data_manager = SQLiteDataManager()

        # Import routes
        from . import routes

    return app
