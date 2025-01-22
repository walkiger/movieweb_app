from app import db
from .data_manager_interface import DataManagerInterface


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
        pass  # Removed db.init_app(app) and db.create_all()
              # to avoid circular issues


    def get_all_users(self):
        """
        Retrieve a list of all users.

        :return: A list of User objects.
        """
        return User.query.all()


    def get_user_by_id(self, user_id):
        """
        Retrieve a user by their unique ID.

        :param user_id: The unique identifier of the user.
        :return: User object or None if not found.
        """
        return User.query.get(user_id)


    def get_user_movies(self, user_id):
        """
        Retrieve a list of movies for a specific user.

        :param user_id: The unique identifier of the user.
        :return: A list of Movie objects.
        """
        return Movie.query.filter_by(user_id=user_id).all()


    def add_user(self, user_name):
        """
        Add a new user to the database.

        :param user_name: The name of the user to add.
        """
        new_user = User(name=user_name)
        db.session.add(new_user)
        db.session.commit()


    def add_movie(self, user_id, movie_name, director, year, rating):
        """
        Add a new movie for a specific user.

        :param user_id: The unique identifier of the user.
        :param movie_name: The name of the movie to add.
        :param director: The director of the movie.
        :param year: The year the movie was released.
        :param rating: The rating of the movie.
        """
        new_movie = Movie(
            user_id=user_id,
            name=movie_name,
            director=director,
            year=year,
            rating=rating
        )
        db.session.add(new_movie)
        db.session.commit()


    def update_movie(self, user_id, movie_id, **kwargs):
        """
        Update details of a specific movie for a user.

        :param user_id: The unique identifier of the user.
        :param movie_id: The unique identifier of the movie.
        :param kwargs: A dictionary of attributes to update.
        """
        movie = Movie.query.filter_by(user_id=user_id, id=movie_id).first()
        if movie:
            for key, value in kwargs.items():
                setattr(movie, key, value)
            db.session.commit()


    def delete_movie(self, user_id, movie_id):
        """
        Delete a movie from a user's collection.

        :param user_id: The unique identifier of the user.
        :param movie_id: The unique identifier of the movie to delete.
        """
        movie = Movie.query.filter_by(user_id=user_id, id=movie_id).first()
        if movie:
            db.session.delete(movie)
            db.session.commit()


    def get_movie_by_id(self, movie_id):
        """
        Retrieve a movie by its unique ID.

        :param movie_id: The unique identifier of the movie.
        :return: Movie object or None if not found.
        """
        return Movie.query.get(movie_id)
