import sqlite3
import os

db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "condominiums.db")

def get_db_conn() -> sqlite3.Connection:
      return sqlite3.connect(db_file)

def search_by_address(conn: sqlite3.Connection, search_term: str) -> list[tuple]:
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

def search_by_name(conn: sqlite3.Connection, search_term: str) -> list[tuple]:
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

def search_list_by_name(conn: sqlite3.Connection, list_names: list[str]) -> list[tuple]:
    results = []
    for name in list_names:
        name = name.strip()
        if not name:
            continue
        results.extend(search_by_name(conn, name))

    return results

def delete_by_id(conn: sqlite3.Connection, condo_id: int) -> tuple | None:
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM
         condominiums
        WHERE
         id = ?
        RETURNING
         *
    ;''', (condo_id,))
    deleted_row = cursor.fetchone()
    conn.commit()

    return deleted_row

def add_condominium(conn: sqlite3.Connection, name: str, address: str) -> tuple | None:
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
