from time import time
import pandas as pd


def try_create_user(conn, user_login, user_password):
    registration_date = int(time())
    conn.execute(f'''
         INSERT INTO
             user (user_login, user_password, registration_date)
         VALUES
             ('{user_login}', '{user_password}', {registration_date})
        ''')
    conn.commit()


def try_get_user_data_by_id(conn, user_id):
    query_result = pd.read_sql(f'''
         SELECT
             user_id,
             user_login,
             registration_date
         FROM
             user
         WHERE
             user_id = {user_id}
        ''', conn)
    return query_result.loc[0] if not query_result.empty else None


def try_get_user_data(conn, user_name, password):
    query_result = pd.read_sql(f'''
         SELECT
             user_id,
             user_login,
             registration_date
         FROM
             user
         WHERE
             user_login = '{user_name}' AND user_password = '{password}'
        ''', conn)
    return query_result.loc[0] if not query_result.empty else None
