from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """
    An interface for data managers to handle user and movie data.
    """

    @abstractmethod
    def get_all_users(self):
        """
        Retrieve a list of all users.

        :return: A list of user dictionaries containing user information.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieve a list of movies for a specific user.

        :param user_id: The unique identifier of the user.
        :return: A list of movie dictionaries containing movie information.
        """
        pass

    @abstractmethod
    def add_user(self, user_name):
        """
        Add a new user.

        :param user_name: The name of the user to add.
        """
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_name, director, year, rating):
        """
        Add a new movie for a specific user.

        :param user_id: The unique identifier of the user.
        :param movie_name: The name of the movie to add.
        :param director: The director of the movie.
        :param year: The year the movie was released.
        :param rating: The rating of the movie.
        """
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, **kwargs):
        """
        Update details of a specific movie for a user.

        :param user_id: The unique identifier of the user.
        :param movie_id: The unique identifier of the movie.
        :param kwargs: A dictionary of attributes to update.
        """
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """
        Delete a movie from a user's collection.

        :param user_id: The unique identifier of the user.
        :param movie_id: The unique identifier of the movie to delete.
        """
        pass
