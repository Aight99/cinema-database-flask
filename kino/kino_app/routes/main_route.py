import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from kino_app import visit_count
from utils import get_db_connection
from kino_app.models.kino_model import *

main = Blueprint('main', __name__)


@main.route('/')
def main_page():
    conn = get_db_connection()

    username = current_user.login if current_user.is_authenticated else None
    movies = get_user_list(conn, username)
    reviews = get_movie_recent_reviews(conn, 7)
    popular = get_popular_today(conn)

    html = render_template(
        'main.html',
        movies=movies,
        reviews=reviews,
        popular=popular,
        len=len,
        range=range,
        notna=pd.notna
    )
    return html


@main.route('/gallery')
def gallery():
    conn = get_db_connection()
    search_query = request.args.get('search_query')
    search_query = search_query.strip() if search_query is not None else ""
    selected_genre = request.args.get('genre_select')
    selected_genre = selected_genre if selected_genre is not None else -1

    movies = get_filtered_movies(conn, search_query, selected_genre)
    genres = get_genres(conn)

    html = render_template(
        'gallery.html',
        movies=movies,
        genres=genres,
        search_query=search_query,
        selected_genre=selected_genre,
        len=len,
        range=range,
        int=int,
        notna=pd.notna
    )
    return html


@login_required
@main.route('/list')
def user_list():
    conn = get_db_connection()

    username = current_user.login
    movies = get_user_list(conn, username, True)

    html = render_template(
        'user_list.html',
        movies=movies,
        len=len,
        range=range,
        notna=pd.notna
    )
    return html


@login_required
@main.route('/add/review', methods=['POST'])
def edit_or_add_review():
    conn = get_db_connection()

    username = current_user.login
    movie_id = request.form.get('movie_id')
    score = request.form.get('rating-10')
    status_id = request.form.get('status')
    text = request.form.get('text')
    text = text if len(text) > 0 else None
    old_review = get_user_review(conn, username, movie_id)
    old_text = old_review['review'] if old_review is not None else None

    if text is None or text == old_text:
        update_list_entry(conn, username, movie_id, status_id, score)
    else:
        add_or_edit_review(conn, username, movie_id, status_id, score, text)

    update_movies_rating(conn)

    return redirect(request.referrer)


@main.route('/movie/<int:movie_id>')
def movie_page(movie_id):
    add_visit(movie_id)
    conn = get_db_connection()

    username = current_user.login if current_user.is_authenticated else None
    movie = get_movie(conn, movie_id)
    genres = get_movie_genres(conn, movie_id)
    crew = get_movie_crew(conn, movie_id)
    crew_by_roles = {role: [(person_id, person_name) for i, person_name, r, person_id in crew.itertuples() if r == role]
                     for role in list(crew['crew_role_name'])}
    reviews = get_movie_reviews(conn, movie_id, 7)
    user_review = get_user_review(conn, username, movie_id)

    html = render_template(
        'movie.html',
        movie=movie.loc[0],
        genres=genres,
        crew=crew_by_roles,
        reviews=reviews,
        user_review=user_review,
        len=len,
        range=range,
        notna=pd.notna,
        none=None
    )
    return html


def add_visit(movie_id):
    if movie_id in visit_count.keys():
        visit_count[movie_id] += 1
    else:
        visit_count[movie_id] = 1
