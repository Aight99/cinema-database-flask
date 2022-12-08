import pandas as pd
from flask import Blueprint, render_template
from utils import get_db_connection
from kino_app.models.kino_model import get_user_list, get_movie

main = Blueprint('main', __name__)


@main.route('/')
def main_page():
    conn = get_db_connection()

    username = 'qwerty'
    movies = get_user_list(conn, username)

    html = render_template(
        'main.html',
        movies=movies,
        len=len,
        range=range,
        notna=pd.notna
    )
    return html


@main.route('/gallery')
def gallery():
    conn = get_db_connection()

    username = 'qwerty'
    movies = get_user_list(conn, username)

    html = render_template(
        'films_template.html',
        movies=movies,
        len=len,
        range=range,
        notna=pd.notna
    )
    return html


@main.route('/movie/<int:movie_id>')
def movie_page(movie_id):
    conn = get_db_connection()

    movie = get_movie(conn, movie_id)

    html = render_template(
        'movie.html',
        movie=movie.loc[0],
        len=len,
        range=range,
        notna=pd.notna
    )
    return html

