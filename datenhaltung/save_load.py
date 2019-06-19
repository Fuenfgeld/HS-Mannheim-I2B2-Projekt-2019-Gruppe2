from datenhaltung import connection


def create_table():
    try:
        conn = connection.create_connection()
    except:
        print ("Verbindung fehlgeschlagen.")
    cur = conn.cursor()
    try:
        cur.execute("DROP TABLE saved")
        cur.execute("CREATE TABLE saved(id serial PRIMARY KEY, name varchar not null, query varchar not null);")
    except:
        print("Erstellen fehlgeschlagen")
    conn.commit()
    conn.close()
    cur.close()

if __name__ == '__main__':
    create_table()
