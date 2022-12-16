import psycopg2


conn = psycopg2.connect(database='netology_db', user='postgres', password='Asdqwerty17')
with conn.cursor() as cur:
    def create_db(conn):
        cur.execute("""
        DROP TABLE phones;
        DROP TABLE clients;
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                name VARCHAR(40),
                surname VARCHAR(40),
                email VARCHAR(60)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
                id SERIAL PRIMARY KEY,
                phone INTEGER,
                client_id INTEGER REFERENCES clients(id)
            );
        """)
        conn.commit()

    def add_client(conn, name, surname, email, phone=None):
        cur.execute("""
                INSERT INTO clients(name, surname, email) VALUES(%s, %s, %s) RETURNING id;
                """, (name, surname, email))
        new_client = cur.fetchone()
        if phone is not None:
            cur.execute("""
                    INSERT INTO phones(client_id, phone) VALUES(%s, %s);
                    """, (new_client[0], phone))
        conn.commit()

    def add_phone(conn, client_id, phone):
        cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES(%s, %s);
        """, (client_id, phone))
        conn.commit()

    def change_client(conn, client_id, name=None, surname=None, email=None, number=None):
        if name is not None:
            cur.execute("""
               UPDATE clients SET name=%s WHERE id=%s; 
            """, (name, client_id))
        if surname is not None:
            cur.execute("""
               UPDATE clients SET surname=%s WHERE id=%s; 
            """, (surname, client_id))
        if email is not None:
            cur.execute("""
               UPDATE clients SET email=%s WHERE id=%s; 
            """, (email, client_id))
        if number is not None:
            cur.execute("""
                UPDATE phones SET phone=%s WHERE client_id=%s;
            """, (number, client_id))
        conn.commit()

    def delete_phone(conn, client_id=None, phone=None):
        ans = input('Вы хотите удалить все номера? (Да|Нет)')
        if ans.lower() == 'нет':
            cur.execute("""
                DELETE FROM phones WHERE phone=%s;
            """, (phone,))
        else:
            cur.execute("""
                DELETE FROM phones WHERE client_id=%s;
            """, (client_id,))
        conn.commit()

    def delete_client(conn, client_id):
        cur.execute("""
            SELECT phone FROM phones WHERE client_id=%s;
        """, (client_id,))
        numb = cur.fetchone()
        if numb is None:
            cur.execute("""
                DELETE FROM clients WHERE id=%s;
            """, (client_id,))
            conn.commit()
        else:
            cur.execute("""
                DELETE FROM phones WHERE client_id=%s;
            """, (client_id,))
            cur.execute("""
                DELETE FROM clients WHERE id=%s;
            """, (client_id,))
            conn.commit()

    def search_client(conn, name=None, surname=None, email=None, number=None):
        if name is not None:
            cur.execute("""
                SELECT * FROM clients WHERE name=%s;
            """, (name,))
            print(cur.fetchall())
        if surname is not None:
            cur.execute("""
                SELECT * FROM clients WHERE surname=%s;
            """, (surname,))
            print(cur.fetchall())
        if email is not None:
            cur.execute("""
                SELECT * FROM clients WHERE email=%s;
            """, (email,))
            print(cur.fetchall())
        if number is not None:
            cur.execute("""
                SELECT client_id FROM phones WHERE phone=%s;
            """, (number, ))
            client_id = cur.fetchone()
            cur.execute("""
                SELECT * FROM clients WHERE id=%s;
            """, (client_id, ))
            print(cur.fetchall())
        conn.commit()


    create_db(conn)
    add_client(conn, 'Ilya', 'Moiseev', 'rger@rger', 235656)
    add_client(conn, 'Danya', 'Muraviev', 'asd@papa')
    add_client(conn, 'Aleksandr', 'Pimanov', 'afrtr@wegfrg')
    add_phone(conn, 1, 14637)
    add_phone(conn, 2, 777777)
    change_client(conn, 2, None, None, 'qtrtry@paa', 111111)
    delete_phone(conn, 1, 14637)
    delete_client(conn, 3)
    search_client(conn, None, None, None, 111111)
