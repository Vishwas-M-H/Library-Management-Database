from html import escape

import streamlit as st

from database import (
    add_book,
    get_books,
    get_category_summary,
    get_most_available_book,
    get_total_available_copies,
    initialize_database,
)


CATEGORIES = [
    "Programming",
    "Artificial Intelligence",
    "Data Science",
    "Mathematics",
    "Electronics",
    "Management",
]


def _save_book():
    category_choice = st.session_state["new_book_category"]
    category = (
        st.session_state["new_book_custom_category"]
        if category_choice == "Other"
        else category_choice
    )
    try:
        add_book(
            st.session_state["new_book_title"],
            st.session_state["new_book_author"],
            category,
            st.session_state["new_book_copies"],
        )
    except ValueError as error:
        st.session_state["book_form_error"] = str(error)
        return

    st.session_state["book_added_notice"] = (
        f'"{st.session_state["new_book_title"].strip()}" was added to the library.'
    )
    st.session_state["new_book_title"] = ""
    st.session_state["new_book_author"] = ""
    st.session_state["new_book_category"] = CATEGORIES[0]
    st.session_state["new_book_custom_category"] = ""
    st.session_state["new_book_copies"] = 1


st.set_page_config(page_title="ABC College Library", page_icon="📖", layout="wide")
initialize_database()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #172a3a;
        --muted: #647789;
        --teal: #087e78;
        --line: #e4ecec;
        --paper: #f5f8f7;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 84% 0%, rgba(201, 232, 224, .42), transparent 34rem),
            var(--paper);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: linear-gradient(175deg, #102d3a 0%, #163b46 65%, #17534f 100%);
    }
    [data-testid="stSidebar"] * { color: #eef8f5; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: .55rem .65rem;
        border-radius: .65rem;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(255,255,255,.1);
    }
    .brand-mark {
        width: 3rem;
        height: 3rem;
        display: grid;
        place-items: center;
        background: rgba(255,255,255,.13);
        border: 1px solid rgba(255,255,255,.19);
        border-radius: 1rem;
        font-size: 1.55rem;
        margin: .5rem 0 1rem;
    }
    .side-label {
        color: #a7c7c4;
        font-size: .69rem;
        font-weight: 700;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin: 1.4rem 0 .45rem;
    }
    .side-note {
        color: #c1d8d4;
        font-size: .84rem;
        line-height: 1.55;
    }
    .hero {
        padding: 2rem 2.2rem;
        margin: .35rem 0 1.5rem;
        border-radius: 1.35rem;
        background: linear-gradient(112deg, #123744 0%, #17615e 72%, #258578 100%);
        color: #f4fbf8;
        box-shadow: 0 18px 42px rgba(20, 67, 69, .14);
        position: relative;
        overflow: hidden;
    }
    .hero:after {
        content: '✦';
        position: absolute;
        right: 3rem;
        top: -.6rem;
        color: rgba(255,255,255,.11);
        font-size: 9rem;
    }
    .eyebrow {
        color: #aee4d7;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .16em;
        text-transform: uppercase;
    }
    .hero h1 {
        color: #fff;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(1.7rem, 3vw, 2.5rem);
        letter-spacing: -.045em;
        margin: .5rem 0;
    }
    .hero p {
        color: #d3e8e4;
        margin: 0;
        max-width: 39rem;
        font-size: .98rem;
    }
    h2, h3 { color: var(--ink); font-family: 'Manrope', sans-serif; }
    [data-testid="stMetric"] {
        background: #fff;
        border: 1px solid var(--line);
        border-radius: 1rem;
        padding: 1.05rem 1.2rem;
        box-shadow: 0 5px 18px rgba(20, 54, 65, .035);
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--ink); }
    [data-testid="stForm"] {
        padding: 1.3rem 1.45rem;
        border: 1px solid var(--line);
        border-radius: 1rem;
        background: #fff;
    }
    .section-kicker {
        color: var(--teal);
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .12em;
        text-transform: uppercase;
        margin-bottom: .15rem;
    }
    .book-highlight {
        background: #fff;
        border: 1px solid var(--line);
        border-left: 4px solid #21a18b;
        border-radius: .8rem;
        padding: 1rem 1.2rem;
    }
    .book-highlight .title {
        font-family: 'Manrope', sans-serif;
        color: var(--ink);
        font-weight: 700;
        font-size: 1.08rem;
    }
    .book-highlight .detail { color: var(--muted); margin-top: .2rem; }
    .stButton > button[kind="primary"],
    [data-testid="stFormSubmitButton"] button {
        background: #087e78;
        border-color: #087e78;
        color: white;
        border-radius: .65rem;
        font-weight: 700;
    }
    .stButton > button[kind="primary"]:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        background: #066a65;
        border-color: #066a65;
        color: white;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: .8rem;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div class="brand-mark">
            <svg viewBox="0 0 64 64" width="38" height="38" role="img"
                 aria-label="ABC Library logo">
                <path d="M12 17.5c7.1-2.5 13.8-1.4 20 3.2v28c-6.2-4.6-12.9-5.7-20-3.2z"
                      fill="#ffffff" stroke="#9bd9c8" stroke-width="2"
                      stroke-linejoin="round"/>
                <path d="M52 17.5c-7.1-2.5-13.8-1.4-20 3.2v28c6.2-4.6 12.9-5.7 20-3.2z"
                      fill="#d0eee4" stroke="#9bd9c8" stroke-width="2"
                      stroke-linejoin="round"/>
                <path d="M32 21v27.5" fill="none" stroke="#087e78"
                      stroke-width="2.5" stroke-linecap="round"/>
                <path d="M18 25.5c3.4-.7 6.7-.3 9.5 1.1M18 31c3.4-.7 6.7-.3 9.5 1.1M46 25.5c-3.4-.7-6.7-.3-9.5 1.1M46 31c-3.4-.7-6.7-.3-9.5 1.1"
                      fill="none" stroke="#65ad9b" stroke-width="1.8"
                      stroke-linecap="round"/>
                <path d="m47 9 1.7 3.6 3.9.5-2.9 2.7.7 3.9-3.4-1.9-3.4 1.9.7-3.9-2.9-2.7 3.9-.5z"
                      fill="#f3c76a"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### ABC Library")
    st.markdown(
        '<div class="side-note">A thoughtful home for every book.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="side-label">Workspace</div>', unsafe_allow_html=True)
    page = st.radio(
        "Go to",
        ["Overview", "Add a book", "View books"],
        format_func=lambda item: {
            "Overview": "⌂   Overview",
            "Add a book": "＋   Add a book",
            "View books": "▤   Browse collection",
        }[item],
        label_visibility="collapsed",
        key="library_page",
    )
    st.markdown("---")
    st.markdown('<div class="side-label">Quick glance</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="side-note"><strong>{get_total_available_copies()}</strong> '
        f'available copies<br><strong>{len(get_books())}</strong> book titles</div>',
        unsafe_allow_html=True,
    )

books = get_books()
categories = get_category_summary()
total_copies = get_total_available_copies()

if page == "Overview":
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">ABC Engineering College · Library</div>
            <h1>Your library, beautifully organized.</h1>
            <p>Keep the collection current, find a title in seconds, and see what
            is on the shelves at a glance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    metric_columns = st.columns(3)
    metric_columns[0].metric("Available copies", f"{total_copies:,}")
    metric_columns[1].metric("Book titles", f"{len(books):,}")
    metric_columns[2].metric("Categories", f"{len(categories):,}")

    left, right = st.columns([1.25, 1], gap="large")
    with left:
        st.markdown("### Category shelves")
        if categories:
            st.bar_chart(
                {item["category"]: item["available_copies"] for item in categories},
                color="#16877d",
                y_label="Available copies",
            )
        else:
            st.info("Your category shelves will appear here when you add books.")
    with right:
        st.markdown("### Most available")
        most_available = get_most_available_book()
        if most_available is None:
            st.info("No books yet. Add your first title to get started.")
        else:
            st.markdown(
                f"""
                <div class="book-highlight">
                    <div class="section-kicker">{escape(most_available['category'])}</div>
                    <div class="title">{escape(most_available['book_title'])}</div>
                    <div class="detail">by {escape(most_available['author_name'])}</div>
                    <div class="detail"><strong>{most_available['available_copies']}</strong>
                    copies on the shelf</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("### Recently added")
        if books:
            for book in reversed(books[-4:]):
                st.text(book["book_title"])
                st.caption(f"{book['author_name']} · {book['category']}")
        else:
            st.caption("New titles will show up here.")

elif page == "Add a book":
    st.markdown(
        '<div class="section-kicker">Grow the collection</div>',
        unsafe_allow_html=True,
    )
    st.title("Add a new book")
    st.caption("Enter the book details below. Your changes are saved to the library immediately.")

    if "book_added_notice" in st.session_state:
        st.success(st.session_state.pop("book_added_notice"))
    if "book_form_error" in st.session_state:
        st.error(st.session_state.pop("book_form_error"))

    st.session_state.setdefault("new_book_title", "")
    st.session_state.setdefault("new_book_author", "")
    st.session_state.setdefault("new_book_category", CATEGORIES[0])
    st.session_state.setdefault("new_book_custom_category", "")
    st.session_state.setdefault("new_book_copies", 1)

    title = st.text_input(
        "Book title",
        max_chars=200,
        placeholder="e.g. Introduction to Algorithms",
        key="new_book_title",
    )
    author = st.text_input(
        "Author name",
        max_chars=150,
        placeholder="e.g. Thomas H. Cormen",
        key="new_book_author",
    )
    category_choice = st.selectbox(
        "Category",
        CATEGORIES + ["Other"],
        key="new_book_category",
    )
    if category_choice == "Other":
        category = st.text_input(
            "Enter category",
            max_chars=100,
            placeholder="Type a category",
            key="new_book_custom_category",
        )
    else:
        st.session_state["new_book_custom_category"] = ""
        category = category_choice

    copies = st.number_input(
        "Available copies",
        min_value=0,
        step=1,
        key="new_book_copies",
    )
    st.button(
        "＋  Add to library",
        type="primary",
        width="stretch",
        on_click=_save_book,
    )

elif page == "View books":
    st.markdown(
        '<div class="section-kicker">Find your next read</div>',
        unsafe_allow_html=True,
    )
    st.title("Browse the collection")
    st.caption("Search titles and authors, or narrow the list by shelf and availability.")

    if books:
        filter_columns = st.columns([2, 1, 1])
        query = filter_columns[0].text_input(
            "Search", placeholder="Search title or author...", label_visibility="collapsed"
        ).strip().casefold()
        category_options = ["All categories"] + sorted(
            {book["category"] for book in books}, key=str.casefold
        )
        selected_category = filter_columns[1].selectbox("Category", category_options)
        stock_filter = filter_columns[2].selectbox(
            "Availability", ["Any stock", "Available", "Out of stock"]
        )

        filtered_books = [
            book
            for book in books
            if (
                not query
                or query in book["book_title"].casefold()
                or query in book["author_name"].casefold()
            )
            and (
                selected_category == "All categories"
                or book["category"].casefold() == selected_category.casefold()
            )
            and (
                stock_filter == "Any stock"
                or (stock_filter == "Available" and book["available_copies"] > 0)
                or (stock_filter == "Out of stock" and book["available_copies"] == 0)
            )
        ]
        result_columns = st.columns(2)
        result_columns[0].metric("Matching titles", len(filtered_books))
        result_columns[1].metric(
            "Copies in results", f"{sum(book['available_copies'] for book in filtered_books):,}"
        )
        if filtered_books:
            st.dataframe(
                filtered_books,
                hide_index=True,
                width="stretch",
                column_config={
                    "book_id": st.column_config.NumberColumn("ID", format="%d"),
                    "book_title": st.column_config.TextColumn("Book title"),
                    "author_name": st.column_config.TextColumn("Author"),
                    "category": st.column_config.TextColumn("Category"),
                    "available_copies": st.column_config.NumberColumn(
                        "Available copies", format="%d"
                    ),
                },
            )
        else:
            st.info("No books match those filters. Try another search or category.")
    else:
        st.info("The shelves are waiting for their first books.")
        if st.button("＋  Add your first book", type="primary"):
            st.session_state["library_page"] = "Add a book"
            st.rerun()
