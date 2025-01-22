from flask import current_app as app
from flask import render_template


@app.route('/')
def home():
    """
    Home route that returns a welcome message.
    """
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    """
    Route to list all users.

    :return: A string representation of the list of users.
    """
    users = app.data_manager.get_all_users()
    user_names = [user.name for user in users]
    return ', '.join(user_names)  # Temporarily returning user names as a string
