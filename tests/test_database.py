import tempfile
import unittest
from pathlib import Path

from database import (
    add_book,
    get_books,
    get_category_summary,
    get_most_available_book,
    get_total_available_copies,
    initialize_database,
)


class LibraryDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temporary_directory.name) / "test_library.db"
        initialize_database(self.database_path)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_empty_database_returns_zero_and_no_most_available_book(self):
        self.assertEqual(get_total_available_copies(self.database_path), 0)
        self.assertIsNone(get_most_available_book(self.database_path))
        self.assertEqual(get_category_summary(self.database_path), [])

    def test_add_and_list_books(self):
        book_id = add_book(
            "Python Basics", "A. Writer", "Programming", 4, self.database_path
        )

        self.assertEqual(book_id, 1)
        self.assertEqual(
            get_books(self.database_path),
            [
                {
                    "book_id": 1,
                    "book_title": "Python Basics",
                    "author_name": "A. Writer",
                    "category": "Programming",
                    "available_copies": 4,
                }
            ],
        )

    def test_inventory_statistics(self):
        add_book("Python Basics", "A. Writer", "Programming", 4, self.database_path)
        add_book("SQL Guide", "B. Writer", "Programming", 2, self.database_path)
        add_book("Algebra", "C. Writer", "Mathematics", 5, self.database_path)

        self.assertEqual(get_total_available_copies(self.database_path), 11)
        self.assertEqual(
            get_most_available_book(self.database_path)["book_title"], "Algebra"
        )
        self.assertEqual(
            get_category_summary(self.database_path),
            [
                {
                    "category": "Mathematics",
                    "book_titles": 1,
                    "available_copies": 5,
                },
                {
                    "category": "Programming",
                    "book_titles": 2,
                    "available_copies": 6,
                },
            ],
        )

    def test_invalid_book_data_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Book title is required"):
            add_book(" ", "A. Writer", "Programming", 1, self.database_path)
        with self.assertRaisesRegex(ValueError, "whole number"):
            add_book("Python Basics", "A. Writer", "Programming", 1.5, self.database_path)
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            add_book("Python Basics", "A. Writer", "Programming", -1, self.database_path)
        self.assertEqual(get_books(self.database_path), [])


if __name__ == "__main__":
    unittest.main()
