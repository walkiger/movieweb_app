from flask import current_app as app
from flask import render_template

@app.route('/')
def home():
    """
    Home route that returns a welcome message.
    """
    return "Welcome to MovieWeb App!"
