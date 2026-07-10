import sqlite3

def get_db_conn() -> sqlite3.Connection:
      return sqlite3.connect("condominiums.db")

def search_by_address(conn, search_term):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
         *
        FROM
         condominiums
        WHERE
         LOWER(address) LIKE LOWER(?)
        ;''', (f"%{search_term}%",)
    )
    rows = cursor.fetchall()

    return rows

def search_by_name(conn, search_term):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
         *
        FROM
         condominiums
        WHERE
         LOWER(name) LIKE LOWER(?)
        ;''', (f"%{search_term}%",)
    )
    rows = cursor.fetchall()

    return rows

def delete_by_id(conn, id):
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM
         condominiums
        WHERE
         id = ?
        RETURNING
         *
    ;''', (id,))
    deleted_row = cursor.fetchone()
    conn.commit()

    return deleted_row

def add_condominium(conn, name, address):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO
         condominiums (name, address)
        VALUES
         (?, ?)
        RETURNING
         *
    ;''', (name, address))
    created_row = cursor.fetchone()
    conn.commit()

    return created_row
