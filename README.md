# ABC Engineering College Library

A small Streamlit application for maintaining a library inventory in SQLite.

## Features

- Add a book with its title, author, category, and available-copy count.
- Browse all book records.
- See the total number of available copies and the most-stocked title.
- Review title counts and copy totals by category.
- Store data in `library.db`, created automatically on first run.

## Requirements

- Python 3.9 or newer
- Git

## Set up and run

From this directory, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run the environment's executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The app opens in a browser. Use the left sidebar to jump between the overview,
book entry form, and searchable collection. The collection can be filtered by
category and whether a title has copies in stock.

## Database design

The `books` table contains:

| Column | Type | Description |
| --- | --- | --- |
| `book_id` | INTEGER | Auto-incrementing primary key |
| `book_title` | TEXT | Required book title |
| `author_name` | TEXT | Required author name |
| `category` | TEXT | Required category |
| `available_copies` | INTEGER | Required non-negative copy count |

## Tests

Run the database tests with the active virtual environment:

```powershell
python -m unittest discover -s tests -v
```

The tests use temporary databases and do not modify the library's `library.db`.

## Git

To start version control in this project folder if it is not already a Git
repository:

```powershell
git init
git add app.py database.py tests requirements.txt README.md PROMPTS.md .gitignore
git commit -m "Build SQLite library management app"
```

Review `git status` before staging to ensure generated files and unrelated
content are not included.
