"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 6/04/2022
"""

import requests, bs4
from database import get_verse, insert_book, insert_chapter, insert_verseversion,\
    insert_verse, get_all_versions, get_chapter, get_version

"""Setup initial parameters."""
url_base = 'https://www.bibliaonline.com.br'
res = requests.get(url_base)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
print("Iniciando a raspagem de dados!")


def get_versions():
    """Get all versions."""
    return get_all_versions()


def get_books():
    """Get books."""
    books = []
    books_link = soup.select('.jss50 .jss51 a')
    for index, book in enumerate(books_link):
        books.append(
            {
                'index': index,
                'name': book.getText(),
                'abbr': book.attrs['href'].split('/')[-1]
            }
        )
    return books


def get_chapters(version, books):
    """Get chapters."""
    for book in books:
        url = f"{url_base}/{version[2]}/{book['abbr']}"
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        chapters = soup.select('.jss1 a')
        book['number_chapters'] = len(chapters)
        book['id'] = insert_book(
            book['name'], book['abbr'],
            book['number_chapters']
        )
    return books


def get_verses(version, books):
    """Get verses."""
    number_verses = 0
    for book in books:
        for i in range(book['number_chapters']):
            url = f"{url_base}/\
                {version[2]}/{book['abbr']}/{str(i+1)}"
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            verses = soup.select('p')
            number_verses += len(verses)
            chapter = get_chapter(book['id'], i+1)
            if chapter is None:
                chapter_id = insert_chapter(book['id'], i+1, str(len(verses)))
            else:
                chapter_id = chapter[0]
            
            for index, verse in enumerate(verses):
                if verse.attrs['class'][0] == 'MuiTypography-root':
                    break
                verse_number = len(str(index + 1))
                verse_text = verse.getText()[verse_number:].strip().replace(
                    "'", "''")
                current_verse = get_verse(book['id'], chapter_id, index+1)
                if current_verse is None:
                    verse_id = insert_verse(book['id'], chapter_id, index+1)
                    insert_verseversion(verse_id, version[0], verse_text)
                else:
                    insert_verseversion(
                        current_verse[0],
                        version[0],
                        verse_text
                    )
                
                print(f"{book['name']} cap {i+1} v. {index + 1} cadastrado!")


if __name__ == '__main__':
    versions = get_versions()
    books = get_books()    
    books = get_chapters_by_book(versions[0], books)
    for version in versions:
        get_verses(version, books)    

    print("Terminado a raspagem de dados!")
