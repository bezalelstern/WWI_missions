from flask import Flask
import logging

from blueprints.mission import mission_bp
from db import connection_pool
from services.normal_service import normalize_db

logging.basicConfig(filename='db_logs.log', level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"
app.register_blueprint(mission_bp, url_prefix="/mission")


# Closing the connection pool when app shuts down
# @app.teardown_appcontext
# def close_pool(exception=None):
#     if connection_pool:
#         connection_pool.closeall()


if __name__ == "__main__":
    # normalize_db()
    app.run(debug=True)
