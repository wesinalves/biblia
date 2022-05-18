"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 6/04/2022
"""

import psycopg2


def insert_book(book_name, book_abbr, book_chapters):
    """Insert a book into the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''INSERT INTO webapp_book ("name", abbreviation, chapters) VALUES ('{book_name}', '{book_abbr}', {book_chapters}) RETURNING id;''')
            book_id = cur.fetchone()[0]
            conn.commit()
            return book_id


def insert_chapter(book_id, chapter_number, verses):
    """Insert a chapter into the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''INSERT INTO webapp_chapter (book_id, "number", verses) VALUES ({book_id}, {chapter_number}, '{verses}') RETURNING id;''')
            chapter_id = cur.fetchone()[0]
            conn.commit()
            return chapter_id


def insert_verse(book_id, chapter_id, version_id, verse_number, verse_text):
    """Insert a verse into the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''INSERT INTO webapp_verse (book_id, chapter_id, "number") VALUES ({book_id},{chapter_id}, {verse_number}) RETURNING id;''')
            verse_id = cur.fetchone()[0]
            conn.commit()
            cur.execute(f'''INSERT INTO webapp_verseversion (verse_id, version_id, "text") VALUES ({verse_id},{version_id}, '{verse_text}') RETURNING id;''')
            conn.commit()
            return verse_id


def get_books():
    """Get all books from the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM webapp_book;''')
            books = cur.fetchall()
            return books


def get_chapters(book_id):
    """Get all chapters from a book."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM webapp_chapter WHERE book_id = {book_id};''')
            chapters = cur.fetchall()
            return chapters
# get_verse_id('1 Coríntios', '1', '1')
# get_chapter_id
# get_book_id
# insert_verse_version