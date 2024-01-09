#!/usr/bin/env python3
"""
Basic Babel setup module.
"""

from flask import Flask, render_template, request
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
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
