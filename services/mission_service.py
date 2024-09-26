import psycopg2
from db import get_db_connection, release_db_connection
from services.logger import log


def get_all_users(find_by=None, value=None, count=None):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        query, params = build_query(find_by, value, count)
        log(f"executing query: {query}, params: {params}")
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        users = cur.fetchall()
        return True, users
    except psycopg2.Error as e:
        # log_error(f'Error: {e}')
        print(e)
        return False
    finally:
        if cur:
            cur.close()
        release_db_connection(conn)


def build_query(find_by=None, value=None, count=None):
    query = """
    SELECT * FROM users
    """
    # columns = {
    #     "id": "id",
    #     "name": "name",
    #     "email": "email",
    # }
    params = tuple()
    if find_by and value:
        encoded_find_by = find_by.split(" ")[0].strip()
        query += f" where {encoded_find_by} = %s"
        # query += f" where {columns[find_by]} = %s"
        params = (value,)
    if count:
        query += f" LIMIT %s"
        params = (*params, count,)
    return query, params