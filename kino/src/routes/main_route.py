import pandas as pd
from flask import Blueprint, render_template
from utils import get_db_connection
from src.models.kino_model import get_user_list

main = Blueprint('main', __name__)


@main.route('/')
def main_page():
    conn = get_db_connection()

    username = 'userman'
    movies = get_user_list(conn, username)

    html = render_template(
        'films_template.html',
        movies=movies,
        len=len,
        range=range,
        notna=pd.notna
    )
    return html

