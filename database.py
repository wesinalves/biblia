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


def insert_verse(book_id, chapter_id, verse_number):
    """Insert a verse into the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''INSERT INTO webapp_verse (book_id, chapter_id, "number") VALUES ({book_id},{chapter_id}, {verse_number}) RETURNING id;''')
            verse_id = cur.fetchone()[0]
            conn.commit()            
            return verse_id

def insert_verseversion(verse_id, version_id, version_text):
    """Insert a version into the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''INSERT INTO webapp_verseversion (verse_id, version_id, "text") VALUES ({verse_id}, {version_id}, '{version_text}') RETURNING id;''')
            conn.commit()
            return


def insert_reference(book, chapter, verse, reference_id, text):
    """Insert a reference into the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''INSERT INTO webapp_reference (verse, reference_id, book, chapter, "text") VALUES ('{verse}', {reference_id}, '{book}', {chapter}, '{text}') RETURNING id;''')
            reference_id = cur.fetchone()[0]
            conn.commit()
            return reference_id


def insert_dictionary(book_abbr, chapter_id, verse, dictionary):
    """Insert a dictionary into the database."""
    if not dictionary:
        return False
    title = dictionary['palavra']
    text = dictionary['descricao'].replace("'", "''")
    book = get_book(book_abbr)    
    verse_id = get_verse(book[0], chapter_id, verse)[0]
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            # select dictionary by title
            cur.execute(f'''SELECT * FROM webapp_dictionary WHERE title = '{title}';''')
            dictionary = cur.fetchone()
            if dictionary:
                dictionary_id = dictionary[0]
                cur.execute(f'''INSERT INTO webapp_versedictionary (verse_id, dictionary_id) VALUES ({verse_id}, {dictionary_id}) RETURNING id;''')
                conn.commit()
            else:
                cur.execute(f'''INSERT INTO webapp_dictionary (title, "text") VALUES ('{title}', '{text}') RETURNING id;''')
                dictionary_id = cur.fetchone()[0]
                conn.commit()
                cur.execute(f'''INSERT INTO webapp_versedictionary (verse_id, dictionary_id) VALUES ({verse_id},{dictionary_id}) RETURNING id;''')
                conn.commit()

            return dictionary


def insert_interlinear(verse_id, interlinear_dict):
    """Insert an interlinear into the database."""
    if not interlinear_dict:
        return False
    strong = interlinear_dict['strong']
    definition = interlinear_dict['definicao']
    origin = interlinear_dict['origem'].replace("'", "''")
    use = interlinear_dict['uso'].replace("'", "''")
    classification = interlinear_dict['classificacao']
    transcription = interlinear_dict['original']
    pronounce = interlinear_dict['transliterado'].replace("'", "''")
    spelling = interlinear_dict['texto'].replace("'", "''")

    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            # select interlinear by strong
            cur.execute(f'''SELECT * FROM webapp_interlinear WHERE strong = '{strong}';''')
            interlinear = cur.fetchone()
            if interlinear:
                cur.execute(f'''SELECT * FROM webapp_verseinterlinear WHERE interlinear_id = {interlinear[0]} and verse_id = {verse_id};''')
                verse_interlinear = cur.fetchone()
                if not verse_interlinear:
                    interlinear_id = interlinear[0]
                    cur.execute(f'''INSERT INTO webapp_verseinterlinear (verse_id, interlinear_id) VALUES ({verse_id}, {interlinear_id}) RETURNING id;''')
                    conn.commit()
            else:
                cur.execute(f'''INSERT INTO webapp_interlinear (strong, definition, origin, use, classification, transcription, pronounce, spelling) VALUES ('{strong}', '{definition}', '{origin}', '{use}', '{classification}', '{transcription}', '{pronounce}', '{spelling}') RETURNING id;''')
                interlinear_id = cur.fetchone()[0]
                conn.commit()
                cur.execute(f'''INSERT INTO webapp_verseinterlinear (verse_id, interlinear_id) VALUES ({verse_id},{interlinear_id}) RETURNING id;''')                
                conn.commit()

            return interlinear


def insert_version(verse_id, version):
    """Insert a version into the database."""
    if version['name'] == 'Nenhum registro encontrado!':
        return False
    
    idiom_id = get_idiom_by_version(version['abbr'])

    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:

            # select version by name
            cur.execute(f'''SELECT * FROM webapp_version WHERE (abbreviation) = '{version['abbr']}';''')
            version_id = cur.fetchone()
            if version_id:
                version_id = version_id[0]
                cur.execute(f'''INSERT INTO webapp_verseversion (verse_id, version_id, text) VALUES ({verse_id}, {version_id}, {version['verse']}) RETURNING id;''')
                conn.commit()
            else:
                cur.execute(f'''INSERT INTO webapp_version (name, abbreviation, idiom_id, "default") VALUES ('{version['name']}','{version['abbr']}', {idiom_id}, false) RETURNING id;''')
                version_id = cur.fetchone()[0]
                conn.commit()
                cur.execute(f'''INSERT INTO webapp_verseversion (verse_id, version_id, text) VALUES ({verse_id}, {version_id}, {version['verse']}) RETURNING id;''')
                conn.commit()

            return version


def insert_only_version(version, idiom_id):
    """Insert a version into the database."""
    if version['name'] == 'Nenhum registro encontrado!':
        return False
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:

            # select version by name
            cur.execute(f'''INSERT INTO webapp_version (name, abbreviation, idiom_id, "default") VALUES ('{version['name']}','{version['abbr']}', {idiom_id}, false) RETURNING id;''')
            version_id = cur.fetchone()[0]
            conn.commit()           

            return version_id


def insert_idiom(idiom):
    """Insert an idiom into the database."""

    name = idiom.split(' ')[0].strip()
    translate = idiom.split(' ')[1].strip()
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            # select idiom by name
            cur.execute(f'''INSERT INTO webapp_idiom (name, native_name, "default") values ('{name}', '{translate}', false) RETURNING id;;''')
            idiom_id = cur.fetchone()[0]
            conn.commit()

            return idiom_id


def get_all_books():
    """Get all books from the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM webapp_book order by id;''')
            books = cur.fetchall()
            return books


def get_chapters_by_book(book_id):
    """Get all chapters from a book."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM webapp_chapter WHERE book_id = {book_id};''')
            chapters = cur.fetchall()
            return chapters


def get_verse(book_id, chapter_id, verse_number):
    """Get a verse from a chapter."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM webapp_verse WHERE book_id = {book_id} AND chapter_id = {chapter_id} AND "number" = {verse_number};''')
            verse = cur.fetchone()
            return verse


def get_idiom_by_version(version_abbr):
    """Get the idiom of a version."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT idiom_id FROM webapp_version WHERE abbreviation = '{version_abbr}';''')
            idiom_id = cur.fetchone()
            return idiom_id[0]


def get_all_versions():
    """Get all versions from the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM webapp_version;''')
            versions = cur.fetchall()
            return versions


def get_chapter(book_id, chapter_number):
    """Get a chapter from a book."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM webapp_chapter WHERE book_id = {book_id} AND "number" = {chapter_number};''')
            chapter = cur.fetchone()
            return chapter


def get_version(version_id):
    """Get a version from the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM webapp_version WHERE id = {version_id};''')
            version = cur.fetchone()
            return version

# get_book_id
def get_book(book_abbr):
    """Get a book from the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM webapp_book WHERE abbreviation = '{book_abbr}';''')
            book = cur.fetchone()
            return book


def get_verseinterlinear(interlinear_id, verse_id):
    """Get a verseinterlinear from the database."""
    with psycopg2.connect("dbname=biblia user=postgres password=postgres host=localhost") as conn:
        with conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM webapp_verseinterlinear WHERE interlinear_id = {interlinear_id} AND verse_id = {verse_id};''')
            verse = cur.fetchone()
            return verse
# insert_verse_version

#oiYV=67+QR