import json
import os
import psycopg2
from flask import Flask, request, jsonify
from os.path import join, dirname
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


app = Flask(__name__)

db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')
db_username = os.environ.get('DB_USERNAME')
db_pwd = os.environ.get('DB_PASSWORD')
db_port = os.environ.get('DB_PORT')


def connect_to_db():
    conn = psycopg2.connect(host=db_host, sslmode='require', port=db_port,
                            user=db_username, dbname=db_name, password=db_pwd)
    return conn


@app.route('/')
def index():
    return 'Live'


@app.route('/subscribers', methods=['POST', 'GET', 'PUT'])
def get_p_train_subscribers():
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'POST':
        data = request.json
        data = jsonify(data)
        email_to_create = data.email
        insert_query = """ INSERT INTO p_train_subscribers (email) VALUES {email_to_create} """
        cur.execute(insert_query)
        conn.commit()
        cur.close()
        conn.close()
        return f'Successfully added {email_to_create} to subscriber list', 200
    if request.method == 'PUT':
        data = request.json
        data = jsonify(data)
        email_to_update = data.email
        update_query = """UPDATE
                            p_train_subscribers
                        SET (email)
                        = (%s)
                      WHERE
                        email = %s"""
        cur.execute(update_query, [email_to_update])
        conn.commit()
        cur.close()
        conn.close()
        return f'Successfully updated {email_to_update}!', 200
    cur.execute('SELECT * FROM p_train_subscribers')
    subscribers = json.loads(json.dumps(cur.fetchall(), indent=4,
                             sort_keys=True, default=str))
    cur.close()
    conn.close()
    return subscribers, 200


@app.route('/subscribers/<subscriber_id>', methods=['DELETE'])
def remove_subscriber(subscriber_id):
    if request.method == 'DELETE':
        conn = connect_to_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        delete_query = """DELETE FROM
                            p_train_subscribers
                        WHERE
                            id = %s"""
        cur.execute(delete_query, [subscriber_id])
        conn.commit()
        cur.close()
        conn.close()
        return 'Subscriber has been removed!', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
