# pesquisa-condominio

Simple Python CLI to search, add and delete condominium records stored in a local SQLite database.

## Requirements

- Python 3.11+
- No external dependencies (uses only the standard library: `sqlite3`, `csv`, `sys`)

## Installation

```bash
git clone https://github.com/<your-user>/pesquisa-condominio.git
cd pesquisa-condominio
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

## Database setup

1. Copy the example CSV and fill it with your own data:

   ```bash
   cp init_db.example.csv init_db.csv
   ```

   Format (semicolon-separated, no header):

   ```text
   NAME;FULL ADDRESS
   ```

2. Create the SQLite database and populate it:

   ```bash
   python init_db.py
   ```

   This creates `condominiums.db` with a `condominiums` table (`id`, `name`, `address`).

## Usage

Run the interactive menu:

```bash
python app.py
```

Available options:

| Option | Action                  |
|--------|-------------------------|
| 1      | Search by address       |
| 2      | Search by name          |
| 3      | Add a new condominium   |
| 4      | Delete by ID            |
| 0      | Exit                    |

## Project structure

```text
.
├── app.py               # CLI entry point (menu loop)
├── db.py                # SQLite access layer
├── init_db.py           # Creates the table and imports the CSV
├── init_db.example.csv  # Sample data to bootstrap the database
├── test_db.py           # Unit tests for the SQLite access layer
└── condominiums.db      # SQLite database (generated, gitignored)
```

## Tests

Tests use `pytest` against an in-memory SQLite database, so they do not touch `condominiums.db`.

Install the dev dependencies inside the virtualenv:

```bash
pip install -e ".[dev]"
```

Run the suite:

```bash
pytest -v
```

## Notes

- `condominiums.db` and `init_db.csv` are gitignored — real data must not be committed.
- Queries use parameter binding, so user input is safe against SQL injection.

## License

MIT — see [LICENSE](LICENSE).
