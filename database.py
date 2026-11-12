import sqlite3
from contextlib import contextmanager
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "library.db"


@contextmanager
def _connect(database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialize_database(database_path=DATABASE_PATH):
    with _connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_title TEXT NOT NULL CHECK (length(trim(book_title)) > 0),
                author_name TEXT NOT NULL CHECK (length(trim(author_name)) > 0),
                category TEXT NOT NULL CHECK (length(trim(category)) > 0),
                available_copies INTEGER NOT NULL CHECK (available_copies >= 0)
            )
            """
        )


def add_book(book_title, author_name, category, available_copies, database_path=DATABASE_PATH):
    title = _required_text(book_title, "Book title")
    author = _required_text(author_name, "Author name")
    book_category = _required_text(category, "Category")

    if isinstance(available_copies, bool) or not isinstance(available_copies, int):
        raise ValueError("Available copies must be a whole number.")
    if available_copies < 0:
        raise ValueError("Available copies cannot be negative.")

    with _connect(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO books (book_title, author_name, category, available_copies)
            VALUES (?, ?, ?, ?)
            """,
            (title, author, book_category, available_copies),
        )
        return cursor.lastrowid


def get_books(database_path=DATABASE_PATH):
    with _connect(database_path) as connection:
        rows = connection.execute(
            """
            SELECT book_id, book_title, author_name, category, available_copies
            FROM books
            ORDER BY book_title COLLATE NOCASE, author_name COLLATE NOCASE, book_id
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_total_available_copies(database_path=DATABASE_PATH):
    with _connect(database_path) as connection:
        row = connection.execute(
            "SELECT COALESCE(SUM(available_copies), 0) AS total FROM books"
        ).fetchone()
    return row["total"]


def get_most_available_book(database_path=DATABASE_PATH):
    with _connect(database_path) as connection:
        row = connection.execute(
            """
            SELECT book_id, book_title, author_name, category, available_copies
            FROM books
            ORDER BY available_copies DESC, book_title COLLATE NOCASE, book_id
            LIMIT 1
            """
        ).fetchone()
    return dict(row) if row is not None else None


def get_category_summary(database_path=DATABASE_PATH):
    with _connect(database_path) as connection:
        rows = connection.execute(
            """
            SELECT
                category,
                COUNT(*) AS book_titles,
                SUM(available_copies) AS available_copies
            FROM books
            GROUP BY category COLLATE NOCASE
            ORDER BY category COLLATE NOCASE
            """
        ).fetchall()
    return [dict(row) for row in rows]


def _required_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required.")
    return value.strip()
