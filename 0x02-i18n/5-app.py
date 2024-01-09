#!/usr/bin/env python3
"""
Basic Babel setup module.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """
    Configuration class.
    """

    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Returns a user dictionary or None if the ID cannot be found."""
    requested_user_id = request.args.get('login_as')
    if requested_user_id:
        return users.get(int(requested_user_id))
    return None


@app.before_request
def before_request() -> None:
    """Executed before all other functions.sets details in flask.g.user."""
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """
    Determine the best-matching language for the user.
    """
    if 'locale' in request.args:
        requested_locale = request.args['locale']
        if requested_locale in app.config['LANGUAGES']:
            return requested_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """
    Route handle for index page
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
