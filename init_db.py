import csv

from db import get_db_conn


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS condominiums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT UNIQUE NOT NULL
        );
    ''')
    conn.commit()

def populate_db(conn):
    with open('init_db.csv', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO condominiums (name, address) VALUES (?, ?)', csv_reader)
    conn.commit()

if __name__ == '__main__':
    conn = get_db_conn()
    create_table(conn)
    populate_db(conn)
