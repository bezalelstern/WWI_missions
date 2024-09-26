from flask import Blueprint, jsonify, request
import psycopg2
from db import get_db_connection, release_db_connection
from services.logger import log_error, log

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
        missions_json = [dict(zip([col[0] for col in cur.description], row)) for row in missions]
        log(f'Getting mission with id: {id}. 200')
        return jsonify({"missions": missions_json}), 200
    except psycopg2.Error as e:
        log_error(f'Error: {e}')
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        if cur:
            cur.close()
        release_db_connection(conn)



@mission_bp.route('/mission', methods=['GET'])
def get_all_missions():
    print('Getting all')
    conn = get_db_connection()
    query = """
           SELECT * FROM mission limit 5000
           """
    try:
        cur = conn.cursor()
        cur.execute(query)
        missions = cur.fetchall()
        json = [dict(zip([col[0] for col in cur.description], row)) for row in missions]
        log(f'Getting all mission. 200')
        return jsonify({"missions": json}), 200
    except psycopg2.Error as e:
        log_error(f'Error: {e}')
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        if cur:
            cur.close()
        release_db_connection(conn)

def make_dict(missions,cur):
    missions_json = []
    for row in missions:
        mission_dict = {}
        for col in cur.description:
            mission_dict[col[0]] = row[col[1]]
        missions_json.append(mission_dict)
    return missions_json