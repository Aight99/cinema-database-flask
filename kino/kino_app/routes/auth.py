from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from utils import get_db_connection
from kino_app.models.auth_model import *

auth = Blueprint('auth', __name__)


class User:
    id = None
    login = None
    registration_date = None

    def load_from_db(self, user_id):
        conn = get_db_connection()
        db_record = try_get_user_data_by_id(conn, user_id)
        self.id = int(db_record['user_id'])
        self.login = str(db_record['user_login'])
        self.registration_date = int(db_record['registration_date'])
        return self

    def create(self, user_data):
        self.id = int(user_data['user_id'])
        self.login = str(user_data['user_login'])
        self.registration_date = int(user_data['registration_date'])
        return self

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __str__(self):
        return f'{self.id}:{self.login}'


@auth.route('/login', methods=['POST'])
def login():
    conn = get_db_connection()
    username = request.form.get('username')
    password = request.form.get('password')
    rememberme = bool(request.form.get('rememberme'))
    user_data = try_get_user_data(conn, username, password)
    if user_data is not None:
        login_user(User().create(user_data), rememberme)
    else:
        flash('Incorrect username or password')
        # if incorrect login -> go to full login page
        # https://flask.palletsprojects.com/en/0.12.x/patterns/flashing/
    return redirect(url_for('main.main_page'))


@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('main.main_page'))


@auth.route('/signup', methods=['POST'])
def sign_up():
    name = request.form.get('username')
    password = request.form.get('password')
    password_again = request.form.get('password_again')
    raise NotImplemented
    # return redirect(url_for('main_page'))
