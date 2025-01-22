import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration class for the Flask application.
    """

    SECRET_KEY = 'e8e715cf5c2f4fb1b19b75b312e6f2a5'  # Example random secret key
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "data", "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
