import time

import pandas as pd
from kino_app import visit_count


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


def get_user_review(conn, username, movie_id):
    query_result = pd.read_sql(f'''
         SELECT
             user_login,
             user_list_movie_rating,
             status_name,
             list.movie_id,
             review
         FROM
             user
             JOIN user_list_movie list ON user.user_id = list.user_id
             JOIN movie ON list.movie_id = movie.movie_id
             JOIN user_status ON list.status_id = user_status.status_id
         WHERE
             user.user_login = '{username}' AND list.movie_id = {movie_id}
         ORDER BY
             user_list_movie_rating DESC
        ''', conn)
    return query_result.loc[0] if not query_result.empty else None


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


def get_movie_recent_reviews(conn, count):
    return pd.read_sql(f'''
         SELECT
             movie_name,
             m.movie_id,
             movie_poster_url,
             user_login,
             u.user_id,
             user_list_movie_rating,
             review,
             upvote_count,
             downvote_count,
             DATE(review_date_unix, 'unixepoch') as review_date
         FROM
             user_list_movie
             JOIN movie m on m.movie_id = user_list_movie.movie_id
             JOIN user u on u.user_id = user_list_movie.user_id
         WHERE
             review IS NOT NULL
         ORDER BY 
             review_date_unix DESC 
         LIMIT 
             {count}
        ''', conn)


def get_movie_reviews(conn, movie_id, count):
    return pd.read_sql(f'''
         SELECT
             movie_name,
             movie.movie_id,
             movie_poster_url,
             user_login,
             list.user_id,
             user_list_movie_rating,
             review,
             upvote_count,
             downvote_count,
             DATE(review_date_unix, 'unixepoch') as review_date
         FROM
             movie
             JOIN user_list_movie list ON movie.movie_id = list.movie_id
             JOIN user ON list.user_id = user.user_id
         WHERE
             movie.movie_id = '{movie_id}'
         ORDER BY
             review_date_unix DESC 
         LIMIT 
             {count}
        ''', conn)


def get_movie(conn, movie_id):
    return pd.read_sql(f'''
         SELECT
             movie_name,
             movie_id,
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


def add_or_edit_review(conn, username, movie_id, status, score, review_text):
    cur = conn.cursor()
    timestamp = int(time.time())
    cur.executescript(f'''
        INSERT OR REPLACE INTO 
            user_list_movie(movie_id, user_id, user_list_movie_rating, status_id, review, review_date_unix)
        VALUES 
            (
                {movie_id},
                (SELECT user_id FROM user WHERE user_login = '{username}'),
                {score},
                {status},
                '{review_text}',
                {timestamp}
            )
        ''')
    conn.commit()


def get_popular_today(conn):
    defaults = [1745960, 6710474, 6741278, 11126994, 13706018, 3398540, 4633694, 816692, 7286456, 3718778]
    visit_results = sorted(visit_count, key=lambda x: visit_count[x], reverse=True)
    visit_len = len(visit_results)
    popular_ids = visit_results[:visit_len] + defaults[visit_len:] if visit_len < 10 else visit_results[:10]
    result = pd.DataFrame()
    for i in popular_ids:
        result = pd.concat([result, get_movie(conn, i)])
    return result.reset_index()
