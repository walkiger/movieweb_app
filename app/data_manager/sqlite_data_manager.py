from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from .data_manager_interface import DataManagerInterface
from app import db


class User(db.Model):
    """
    Model representing a user in the database.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)


class Movie(db.Model):
    """
    Model representing a movie in the database.
    """
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)


class SQLiteDataManager(DataManagerInterface):
    """
    Data manager class that implements the DataManagerInterface using SQLite
    with SQLAlchemy.
    """

    def __init__(self):
        """
        Initialize the SQLiteDataManager.
        """
        pass  # No initialization needed here

    def get_all_users(self):
        """
        Retrieve a list of all users.

        :return: A list of User objects.
        """
        try:
            users = User.query.all()
            return users
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in get_all_users: {e}")
            return []

    def get_user_by_id(self, user_id):
        """
        Retrieve a user by their unique ID.

        :param user_id: The unique identifier of the user.
        :return: User object or None if not found.
        """
        try:
            user = User.query.get(user_id)
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in get_user_by_id: {e}")
            return None

    def get_user_movies(self, user_id):
        """
        Retrieve a list of movies for a specific user.

        :param user_id: The unique identifier of the user.
        :return: A list of Movie objects.
        """
        try:
            movies = Movie.query.filter_by(user_id=user_id).all()
            return movies
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in get_user_movies: {e}")
            return []

    def add_user(self, user_name):
        """
        Add a new user to the database.

        :param user_name: The name of the user to add.
        """
        try:
            new_user = User(name=user_name)
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in add_user: {e}")
            raise

    def add_movie(self, user_id, movie_name, director, year, rating):
        """
        Add a new movie for a specific user.

        :param user_id: The unique identifier of the user.
        :param movie_name: The name of the movie to add.
        :param director: The director of the movie.
        :param year: The year the movie was released.
        :param rating: The rating of the movie.
        """
        try:
            new_movie = Movie(
                user_id=user_id,
                name=movie_name,
                director=director,
                year=year,
                rating=rating
            )
            db.session.add(new_movie)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in add_movie: {e}")
            raise


    def update_movie(self, user_id, movie_id, **kwargs):
        """
        Update details of a specific movie for a user.

        :param user_id: The unique identifier of the user.
        :param movie_id: The unique identifier of the movie.
        :param kwargs: A dictionary of attributes to update.
        """
        try:
            movie = Movie.query.filter_by(user_id=user_id, id=movie_id).first()
            if movie:
                for key, value in kwargs.items():
                    if hasattr(movie, key):
                        setattr(movie, key, value)
                db.session.commit()
            else:
                current_app.logger.warning(f"Movie {movie_id} not found for user {user_id}.")
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in update_movie: {e}")
            raise

    def delete_movie(self, user_id, movie_id):
        """
        Delete a movie from a user's collection.

        :param user_id: The unique identifier of the user.
        :param movie_id: The unique identifier of the movie to delete.
        """
        try:
            movie = Movie.query.filter_by(user_id=user_id, id=movie_id).first()
            if movie:
                db.session.delete(movie)
                db.session.commit()
            else:
                current_app.logger.warning(f"Movie {movie_id} not found for user {user_id}.")
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in delete_movie: {e}")
            raise

    def get_movie_by_id(self, movie_id):
        """
        Retrieve a movie by its unique ID.

        :param movie_id: The unique identifier of the movie.
        :return: Movie object or None if not found.
        """
        try:
            movie = Movie.query.get(movie_id)
            return movie
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in get_movie_by_id: {e}")
            return None
