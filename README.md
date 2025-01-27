# Movie Project

## Purpose
This project is a movie management application that allows users to list, add, delete, update, and search for movies. The application provides a web interface for managing your movie collection.

## Setup

### Prerequisites
- Python 3.x installed on your machine

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/walkiger/movieweb_app.git
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
    ```
3. Create a config.py file in the root directory and add the necessary configurations::
    ```python
   import os

   basedir = os.path.abspath(os.path.dirname(__file__))

   class Config:
    """
    Configuration class for the Flask application.
    """
   
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'data', 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   ```
### Usage
1. Run the application:
    ```bash
    python app.py
   ```
2. Access the web interface in your browser at:
    ```
   http://127.0.0.1:5000/
   ```
3. Use the web interface to list, add, delete, update, and search for movies.
### License
This project is licensed under the MIT License.
