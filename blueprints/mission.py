from flask import Blueprint, jsonify, request
import psycopg2
from db import get_db_connection, release_db_connection


mission_bp = Blueprint("mission", __name__)




@mission_bp.route('/mission/<int:id>', methods=['GET'])
def get_missions(id):
    conn = get_db_connection()
    query = """
       SELECT * FROM mission where mission_id = %s; 
       """
    params = (id,)
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        missions = cur.fetchall()
        return jsonify({"missions": missions}), 200
    except psycopg2.Error as e:
        # log_error(f'Error: {e}')
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        if cur:
            cur.close()
        release_db_connection(conn)



@mission_bp.route('/mission', methods=['GET'])
def get_all_missions():
    conn = get_db_connection()
    query = """
           SELECT * FROM mission
           """
    try:
        cur = conn.cursor()
        cur.execute(query)
        missions = cur.fetchall()
        return jsonify({"missions": missions}), 200
    except psycopg2.Error as e:

        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        if cur:
            cur.close()
        release_db_connection(conn)