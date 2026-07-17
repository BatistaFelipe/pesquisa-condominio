import sqlite3
from collections.abc import Iterator

import pytest

from db import (
    add_condominium,
    delete_by_id,
    search_by_address,
    search_by_name,
)


@pytest.fixture
def conn() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE condominiums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT UNIQUE NOT NULL
        );
        """
    )
    connection.executemany(
        "INSERT INTO condominiums (name, address) VALUES (?, ?);",
        [
            ("CONDOMINIO ALPHA", "Rua das Flores, 100 - Centro"),
            ("CONDOMINIO BETA", "Avenida Principal, 250 - Bairro Norte"),
            ("RESIDENCIAL DELTA", "Travessa das Palmeiras, 12 - Jardim Leste"),
        ],
    )
    connection.commit()
    yield connection
    connection.close()


def test_add_condominium_returns_inserted_row(conn: sqlite3.Connection) -> None:
    new_row = add_condominium(conn, "CONDOMINIO NOVO", "Rua Teste, 1")

    assert new_row[1] == "CONDOMINIO NOVO"
    assert new_row[2] == "Rua Teste, 1"
    assert isinstance(new_row[0], int)


def test_add_condominium_persists_to_database(conn: sqlite3.Connection) -> None:
    add_condominium(conn, "CONDOMINIO PERSISTIDO", "Rua Persistencia, 42")

    rows = search_by_name(conn, "persistido")

    assert len(rows) == 1
    assert rows[0][1] == "CONDOMINIO PERSISTIDO"


def test_add_condominium_with_duplicate_address_raises(
    conn: sqlite3.Connection,
) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        add_condominium(conn, "OUTRO NOME", "Rua das Flores, 100 - Centro")


def test_search_by_name_is_case_insensitive(conn: sqlite3.Connection) -> None:
    rows = search_by_name(conn, "alpha")

    assert len(rows) == 1
    assert rows[0][1] == "CONDOMINIO ALPHA"


def test_search_by_name_returns_partial_matches(conn: sqlite3.Connection) -> None:
    rows = search_by_name(conn, "condominio")

    assert len(rows) == 2


def test_search_by_name_returns_empty_when_no_match(
    conn: sqlite3.Connection,
) -> None:
    rows = search_by_name(conn, "inexistente")

    assert rows == []


def test_search_by_address_is_case_insensitive(conn: sqlite3.Connection) -> None:
    rows = search_by_address(conn, "AVENIDA PRINCIPAL")

    assert len(rows) == 1
    assert rows[0][1] == "CONDOMINIO BETA"


def test_search_by_address_returns_partial_matches(
    conn: sqlite3.Connection,
) -> None:
    rows = search_by_address(conn, "bairro")

    assert len(rows) == 1


def test_delete_by_id_removes_row(conn: sqlite3.Connection) -> None:
    deleted = delete_by_id(conn, 1)

    assert deleted is not None
    assert deleted[0] == 1
    assert search_by_name(conn, "alpha") == []


def test_delete_by_id_returns_none_when_not_found(
    conn: sqlite3.Connection,
) -> None:
    deleted = delete_by_id(conn, 9999)

    assert deleted is None
