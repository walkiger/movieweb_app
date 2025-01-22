from flask import current_app as app
from flask import render_template, request, redirect, url_for, abort


@app.errorhandler(404)
def page_not_found(error):
    """
    Error handler for 404 Not Found.

    :param error: The error object.
    :return: Renders the 404.html template with a 404 status code.
    """
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Error handler for 405 Method Not Allowed.

    :param error: The error object.
    :return: Renders the 405.html template with a 405 status code.
    """
    return render_template('405.html'), 405


@app.errorhandler(500)
def internal_server_error(error):
    """
    Error handler for 500 Internal Server Error.

    :param error: The error object.
    :return: Renders the 500.html template with a 500 status code.
    """
    return render_template('500.html'), 500


@app.route('/')
def home():
    """
    Home route that returns a welcome message.
    """
    return render_template('index.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Route to add a new user to the database.

    :return: Renders the add_user.html template or redirects to the users list.
    """
    try:
        if request.method == 'POST':
            user_name = request.form.get('name')
            if user_name:
                app.data_manager.add_user(user_name)
                return redirect(url_for('list_users'))
            else:
                error_message = "User name is required."
                return render_template('add_user.html', error=error_message)
        return render_template('add_user.html')
    except Exception as e:
        app.logger.error(f"Error adding user: {e}")
        abort(500)


@app.route('/users')
def list_users():
    """
    Route to display a list of all users.

    :return: Rendered HTML page with the list of users.
    """
    try:
        users = app.data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        app.logger.error(f"Error fetching users: {e}")
        abort(500)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Route to display a user's list of favorite movies.

    :param user_id: The unique identifier of the user.
    :return: Rendered HTML page with the user's movies.
    """
    try:
        user = app.data_manager.get_user_by_id(user_id)
        if user is None:
            app.logger.warning(f"User with ID {user_id} not found.")
            abort(404)
        movies = app.data_manager.get_user_movies(user_id)
        return render_template('user_movies.html', user=user, movies=movies)
    except Exception as e:
        app.logger.error(f"Error fetching movies for user {user_id}: {e}")
        abort(500)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Route to add a new movie to a user's list.

    :param user_id: The unique identifier of the user.
    :return: Renders the add_movie.html template or redirects to the user's movies.
    """
    try:
        user = app.data_manager.get_user_by_id(user_id)
        if user is None:
            app.logger.warning(f"User with ID {user_id} not found.")
            abort(404)

        if request.method == 'POST':
            movie_name = request.form.get('name')
            director = request.form.get('director')
            year = request.form.get('year')
            rating = request.form.get('rating')

            if not all([movie_name, director, year, rating]):
                error_message = "All fields are required."
                return render_template('add_movie.html', user=user, error=error_message)

            try:
                year = int(year)
                rating = float(rating)
            except ValueError:
                error_message = "Year must be an integer and rating must be a number."
                return render_template('add_movie.html', user=user, error=error_message)

            app.data_manager.add_movie(
                user_id=user_id,
                movie_name=movie_name,
                director=director,
                year=year,
                rating=rating
            )
            return redirect(url_for('user_movies', user_id=user_id))
        return render_template('add_movie.html', user=user)
    except Exception as e:
        app.logger.error(f"Error adding movie for user {user_id}: {e}")
        abort(500)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Route to update an existing movie's details.

    :param user_id: The unique identifier of the user.
    :param movie_id: The unique identifier of the movie.
    :return: Renders the update_movie.html template or redirects to the user's movies.
    """
    try:
        user = app.data_manager.get_user_by_id(user_id)
        if user is None:
            app.logger.warning(f"User with ID {user_id} not found.")
            abort(404)

        movie = app.data_manager.get_movie_by_id(movie_id)
        if movie is None or movie.user_id != user_id:
            app.logger.warning(f"Movie with ID {movie_id} not found for user {user_id}.")
            abort(404)

        if request.method == 'POST':
            movie_name = request.form.get('name')
            director = request.form.get('director')
            year = request.form.get('year')
            rating = request.form.get('rating')

            if not all([movie_name, director, year, rating]):
                error_message = "All fields are required."
                return render_template('update_movie.html', user=user, movie=movie, error=error_message)

            try:
                year = int(year)
                rating = float(rating)
            except ValueError:
                error_message = "Year must be an integer and rating must be a number."
                return render_template('update_movie.html', user=user, movie=movie, error=error_message)

            app.data_manager.update_movie(
                user_id=user_id,
                movie_id=movie_id,
                name=movie_name,
                director=director,
                year=year,
                rating=rating
            )
            return redirect(url_for('user_movies', user_id=user_id))
        return render_template('update_movie.html', user=user, movie=movie)
    except Exception as e:
        app.logger.error(f"Error updating movie {movie_id} for user {user_id}: {e}")
        abort(500)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Route to delete a movie from a user's list.

    :param user_id: The unique identifier of the user.
    :param movie_id: The unique identifier of the movie.
    :return: Redirects to the user's movies.
    """
    try:
        user = app.data_manager.get_user_by_id(user_id)
        if user is None:
            app.logger.warning(f"User with ID {user_id} not found.")
            abort(404)

        movie = app.data_manager.get_movie_by_id(movie_id)
        if movie is None or movie.user_id != user_id:
            app.logger.warning(f"Movie with ID {movie_id} not found for user {user_id}.")
            abort(404)

        app.data_manager.delete_movie(user_id=user_id, movie_id=movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        app.logger.error(f"Error deleting movie {movie_id} for user {user_id}: {e}")
        abort(500)


@app.route('/trigger-error')
def trigger_error():
    """
    Route to deliberately trigger an internal server error for testing purposes.
    """
    raise Exception("Testing 500 Internal Server Error")
