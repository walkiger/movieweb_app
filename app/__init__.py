from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

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
        db.create_all()
        app.data_manager = SQLiteDataManager()

        # Import routes
        from . import routes

    return app
