from flask import current_app as app
from flask import render_template, request, redirect, url_for


@app.route('/')
def home():
    """
    Home route that returns a welcome message.
    """
    return "Welcome to MovieWeb App!"


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Route to add a new user to the database.

    :return: Renders the add_user.html template or redirects to the users list.
    """
    if request.method == 'POST':
        user_name = request.form.get('name')
        if user_name:
            app.data_manager.add_user(user_name)
            return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users')
def list_users():
    """
    Route to display a list of all users.

    :return: Rendered HTML page with the list of users.
    """
    users = app.data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Route to display a user's list of favorite movies.

    :param user_id: The unique identifier of the user.
    :return: Rendered HTML page with the user's movies.
    """
    user = app.data_manager.get_user_by_id(user_id)
    if user is None:
        return "User not found.", 404
    movies = app.data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Route to add a new movie to a user's list.

    :param user_id: The unique identifier of the user.
    :return: Rendered HTML form to add a movie or redirects to the user's movies.
    """
    # Implementation will be added later
    pass


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Route to update an existing movie's details.

    :param user_id: The unique identifier of the user.
    :param movie_id: The unique identifier of the movie.
    :return: Rendered HTML form to update the movie or redirects to the user's movies.
    """
    # Implementation will be added later
    pass


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Route to delete a movie from a user's list.

    :param user_id: The unique identifier of the user.
    :param movie_id: The unique identifier of the movie.
    :return: Redirects to the user's movies.
    """
    # Implementation will be added later
    pass
