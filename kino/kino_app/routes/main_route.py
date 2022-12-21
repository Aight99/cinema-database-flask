import pandas as pd
from flask import Blueprint, render_template
from utils import get_db_connection
from kino_app.models.kino_model import *

main = Blueprint('main', __name__)


@main.route('/')
def main_page():
    conn = get_db_connection()

    username = 'qwerty'
    movies = get_user_list(conn, username)
    reviews = get_movie_recent_reviews(conn, 7)

    html = render_template(
        'main.html',
        movies=movies,
        reviews=reviews,
        len=len,
        range=range,
        notna=pd.notna
    )
    return html


@main.route('/gallery')
def gallery():
    conn = get_db_connection()

    movies = get_all_movies(conn)

    html = render_template(
        'gallery.html',
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
    genres = get_movie_genres(conn, movie_id)
    crew = get_movie_crew(conn, movie_id)
    crew_by_roles = {role: [(person_id, person_name) for i, person_name, r, person_id in crew.itertuples() if r == role]
                     for role in list(crew['crew_role_name'])}
    reviews = get_movie_reviews(conn, movie_id, 7)

    html = render_template(
        'movie.html',
        movie=movie.loc[0],
        genres=genres,
        crew=crew_by_roles,
        reviews=reviews,
        len=len,
        range=range,
        notna=pd.notna
    )
    return html
