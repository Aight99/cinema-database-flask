import sqlite3
import pandas as pd


def create_all_tables(con):
    con.executescript(
        '''
        CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_login TEXT,
        user_password TEXT,
        registration_date INT
        );
        
        CREATE TABLE IF NOT EXISTS user_status (
        status_id INTEGER PRIMARY KEY AUTOINCREMENT,
        status_name TEXT
        );
        
        CREATE TABLE IF NOT EXISTS movie_type (
        movie_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_type_name TEXT
        );
        
        CREATE TABLE IF NOT EXISTS crew_role (
        crew_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        crew_role_name TEXT
        );
        
        CREATE TABLE IF NOT EXISTS person (
        person_id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_name TEXT,
        person_rating REAL
        );
        
        CREATE TABLE IF NOT EXISTS genre (
        genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre_name TEXT
        );
        
        CREATE TABLE IF NOT EXISTS movie (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_name TEXT,
        movie_rating REAL,
        movie_release_year INT,
        movie_duration_minutes INT,
        movie_description TEXT,
        movie_type_id INT,
        FOREIGN KEY (movie_type_id) REFERENCES movie_type (movie_type_id) ON DELETE CASCADE
        );
        
        CREATE TABLE IF NOT EXISTS user_list_movie (
        movie_id INT,
        user_id INT,
        user_list_movie_rating INT,
        status_id INT,
        review TEXT,
        FOREIGN KEY (movie_id) REFERENCES movie (movie_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE,
        FOREIGN KEY (status_id) REFERENCES user_status (status_id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, user_id)
        );
        
        CREATE TABLE IF NOT EXISTS user_list_crew_member (
        movie_id INT,
        user_id INT,
        person_id INT,
        user_list_crew_member_rating INT,
        FOREIGN KEY (movie_id) REFERENCES user_list_movie (movie_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES user_list_movie (user_id) ON DELETE CASCADE,
        FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, user_id, person_id)
        );
        
        CREATE TABLE IF NOT EXISTS crew_member (
        person_id INT,
        movie_id INT,
        crew_role_id INT,
        FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE CASCADE,
        FOREIGN KEY (movie_id) REFERENCES movie (movie_id) ON DELETE CASCADE,
        FOREIGN KEY (crew_role_id) REFERENCES crew_role (crew_role_id) ON DELETE CASCADE,
        PRIMARY KEY (person_id, movie_id, crew_role_id)
        );
        
        CREATE TABLE IF NOT EXISTS movie_genre (
        genre_id INT,
        movie_id INT,
        FOREIGN KEY (genre_id) REFERENCES genre (genre_id) ON DELETE CASCADE,
        FOREIGN KEY (movie_id) REFERENCES movie (movie_id) ON DELETE CASCADE,
        PRIMARY KEY (genre_id, movie_id)
        );
        '''
    )
    con.commit()


# Два запроса на выборку для связанных таблиц с условиями и сортировкой: (JOIN)
# 1. Выборка всех фильмов в списке пользователя по user_id (movie_name, movie_release_year, user_rating, status_name)
# 2. Выборка всех отзывов по фильму
# Два запроса с группировкой и групповыми функциями; (GROUP BY)
# 1. Количество фильмов у пользователя по каждому из статусов
# 2. Количество отзывов и статусов у фильма
# Два запроса со вложенными запросами или табличными выражениями; (WITH ...)
# 1.
# 2.
# Два запроса корректировки данных (обновление, добавление, удаление и пр):
# 1. Обновление рейтинга у фильма, на основе всех рецензий по фильму от пользователей
# 2. Обновление рейтинга у человека, на основе всех рецензий по фильмам с участием человека от пользователей
def execute_smth(con):
    con.executescript(
        '''
        
        '''
    )
    con.commit()


if __name__ == '__main__':
    connection = sqlite3.connect("kino.sqlite")
    cursor = connection.cursor()

    # create_all_tables(connection)

    connection.close()

