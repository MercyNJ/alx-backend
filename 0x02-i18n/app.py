#!/usr/bin/env python3
"""
Basic Babel setup module.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
from datetime import datetime
from flask_babel import format_datetime


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

    if g.user and 'locale' in g.user and g.user['locale'] in \
            app.config['LANGUAGES']:
        return g.user['locale']

    header_locale = request.headers.get('Accept-Language')
    if header_locale:
        header_locale = header_locale.split(',')[0].strip()
        if header_locale in app.config['LANGUAGES']:
            return header_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    Determine the best-matching time zone for the user.
    """
    url_timezone = request.args.get('timezone')
    if url_timezone:
        try:
            pytz.timezone(url_timezone)
            return url_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user and 'timezone' in g.user:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return (app.config['BABEL_DEFAULT_TIMEZONE'])


@app.route('/')
def index():
    """
    Route handle for index page
    """
    current_time = datetime.now(pytz.timezone(get_timezone()))
    formatted_time = format_datetime(current_time)

    return render_template('index.html', current_time=formatted_time)


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
