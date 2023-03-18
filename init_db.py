from app import connect_to_db

conn = connect_to_db()

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS p_train_subscribers;')
cur.execute('CREATE TABLE p_train_subscribers (id serial PRIMARY KEY,'
            'email varchar (150) UNIQUE NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP,'
            'date_updated date DEFAULT CURRENT_TIMESTAMP);'
            )
insert_query = """ INSERT INTO p_train_subscribers (email) VALUES ('aolie94@gmail.com') """

cur.execute(insert_query)
conn.commit()

cur.close()
conn.close()
