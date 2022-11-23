from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return 'I am inside'


@auth.route('/logout')
def logout():
    return 'Kick back'


@auth.route('/reg')
def register():
    return 'Where your snils'
