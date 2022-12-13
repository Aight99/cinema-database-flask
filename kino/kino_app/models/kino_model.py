import pandas as pd


# def get_filtered_movies(conn, genre_ids, author_ids, publisher_ids):
#     genre_ids = tuple(genre_ids * 2)
#     is_genres_empty = is_filter_empty(genre_ids)
#     author_ids = tuple(author_ids * 2)
#     is_authors_empty = is_filter_empty(author_ids)
#     publisher_ids = tuple(publisher_ids * 2)
#     is_publishers_empty = is_filter_empty(publisher_ids)
#     return pd.read_sql(
#         f'''SELECT
#                 title AS Название,
#                 GROUP_CONCAT(author_name, ', ') AS Авторы,
#                 genre_name AS Жанр,
#                 publisher_name AS Издательство,
#                 year_publication AS "Год издания",
#                 available_numbers AS Количество
#             FROM
#                 book
#                 JOIN book_author ba on book.book_id = ba.book_id
#                 JOIN author a on a.author_id = ba.author_id
#                 JOIN genre g on book.genre_id = g.genre_id
#                 JOIN publisher p on book.publisher_id = p.publisher_id
#             GROUP BY
#                 book.book_id
#             HAVING
#                 (g.genre_id IN {genre_ids} OR {is_genres_empty}) AND
#                 (a.author_id IN {author_ids} OR {is_authors_empty}) AND
#                 (p.publisher_id IN {publisher_ids} OR {is_publishers_empty})
#             ''', conn)


def is_filter_empty(id_list):
    if len(id_list) == 0:
        return "TRUE"
    else:
        return "FALSE"


def get_user_list(conn, username):
    return pd.read_sql(f'''
         SELECT
             movie_name,
             user_login,
             user_list_movie_rating,
             status_name,
             movie_poster_url,
             movie_release_year,
             movie_type_name,
             list.movie_id
         FROM
             user
             JOIN user_list_movie list ON user.user_id = list.user_id
             JOIN movie ON list.movie_id = movie.movie_id
             JOIN user_status ON list.status_id = user_status.status_id
             JOIN movie_type mt on movie.movie_type_id = mt.movie_type_id
         WHERE
             user.user_login = '{username}'
         ORDER BY
             user_list_movie_rating DESC
        ''', conn)


def get_all_movies(conn):
    return pd.read_sql(f'''
         SELECT
             movie_name,
             movie_poster_url,
             movie_release_year,
             movie_id,
             movie_type_name
         FROM
             movie
             JOIN movie_type mt on movie.movie_type_id = mt.movie_type_id
        ORDER BY 
            movie_release_year DESC 
        ''', conn)


def get_movie_reviews(conn, film):
    return pd.read_sql(f'''
         SELECT
             movie_name,
             user_login,
             user_list_movie_rating,
             review
         FROM
             movie
             JOIN user_list_movie list ON movie.movie_id = list.movie_id
             JOIN user ON list.user_id = user.user_id
         WHERE
             movie.movie_name = '{film}'
        ''', conn)


def get_movie(conn, movie_id):
    return pd.read_sql(f'''
         SELECT
             movie_name,
             movie_release_year,
             movie_description,
             movie_poster_url,
             movie_type_name,
             movie_duration_minutes,
             movie_rating
         FROM
             movie
             JOIN movie_type mt on movie.movie_type_id = mt.movie_type_id
         WHERE
             movie.movie_id = '{movie_id}'
        ''', conn)


def get_movie_crew(conn, movie_id):
    return pd.read_sql(f'''
         SELECT
             person_name,
             crew_role_name,
             p.person_id
         FROM
             crew_member
             JOIN crew_role cr on cr.crew_role_id = crew_member.crew_role_id
             JOIN person p on p.person_id = crew_member.person_id
         WHERE
             crew_member.movie_id = '{movie_id}'
        ''', conn)


def get_movie_genres(conn, movie_id):
    return pd.read_sql(f'''
         SELECT
             g.genre_id,
             genre_name
         FROM
             movie_genre
             JOIN genre g on movie_genre.genre_id = g.genre_id
         WHERE
             movie_id = '{movie_id}'
        ''', conn)
