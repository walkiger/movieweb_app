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
        # Import routes and initialize the database
        from . import routes
        db.create_all()

    return app
