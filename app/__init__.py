from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    """
    Factory function to create and configure the Flask application.

    :return: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # Import models before creating tables
        from .data_manager.sqlite_data_manager import User, Movie
        db.create_all()

        # Instantiate the data manager
        from .data_manager.sqlite_data_manager import SQLiteDataManager
        app.data_manager = SQLiteDataManager()

        # Import routes
        from . import routes

    return app
