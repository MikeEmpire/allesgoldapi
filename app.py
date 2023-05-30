import json
import os
import psycopg2
import smtplib
from flask import Flask, request
from psycopg2.extras import RealDictCursor
from email.message import EmailMessage


app = Flask(__name__)

db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')
db_username = os.environ.get('DB_USERNAME')
db_pwd = os.environ.get('DB_PASSWORD')
db_port = os.environ.get('DB_PORT')
email_username = os.environ.get('EMAIL_USERNAME')
email_password = os.environ.get('EMAIL_PASSWORD')
destination_email = os.environ.get('DESTINATION_EMAIL')


def connect_to_db():
    conn = psycopg2.connect(host=db_host, sslmode='require', port=db_port,
                            user=db_username, dbname=db_name, password=db_pwd)
    return conn


@app.route('/')
def index():
    return 'Live'


@app.route('/contact', methods=['POST'])
def receive_email():
    # get data and send email to specific email
    contact_name = request.json['name']
    contact_email = request.json['email']
    contact_message = request.json['message']

    email_message = EmailMessage()
    email_message['subject'] = 'New Contact Message from P Train\'s BBQ Train'
    email_message['From'] = contact_email
    email_message['To'] = destination_email
    email_message.set_content(
        f"Name: {contact_name}\nEmail: {contact_email}\nMessage: {contact_message}")

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(email_username, email_password)
        smtp.send_message(email_message)

    return {"message": "success"}, 200


@app.route('/subscribers', methods=['POST', 'GET', 'PUT'])
def get_p_train_subscribers():
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'POST':
        data = request.json['email']
        if data is None:
            return 'Please provide a valid email', 400
        email_to_create = data
        insert_query = f""" INSERT INTO p_train_subscribers (email) VALUES ('{email_to_create}') """
        cur.execute(insert_query)
        conn.commit()
        cur.close()
        conn.close()
        return f'Successfully added {email_to_create} to subscriber list', 200
    if request.method == 'PUT':
        data = request.json['email']
        email_to_update = data
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
    app.run(host='0.0.0.0', port=8080)
