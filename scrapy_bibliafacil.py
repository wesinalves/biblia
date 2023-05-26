"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 6/04/2022
"""

import requests, bs4
from database import get_verse, insert_verseversion,\
    insert_verse, get_chapter, get_all_books
import math

"""Setup initial parameters."""
url_base = 'https://pesquisa.biblia.com.br/pt-BR'
res = requests.get(url_base, verify=False)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
print("Iniciando a raspagem de dados!")


def get_verses(version, books):
    """Get verses."""
    number_verses = 0
    for book in books:        
        for i in range(book[3]):
            chapter = get_chapter(book[0], i+1)
            chapter_id = chapter[0]
            total_verses = chapter[2]
            pages = math.floor(total_verses / 10)
            if total_verses % 10 > 0:
                pages += 1
            for page in range(pages):
                url = f"{url_base}/{version}/{book[2]}/{str(i+1)}?page={page + 1}"
                print(url)
                res = requests.get(url, verify=False)
                soup = bs4.BeautifulSoup(res.text, 'html.parser')
                verses = soup.select(".versiculoTexto")                
                number_verses += len(verses)
                
                for verse in verses:                
                    
                    verse_number = verse.a.text.strip()
                    verse_text = verse.span.next_sibling.strip().replace(
                        "'", "''")
                    
                    current_verse = get_verse(book[0], chapter_id, verse_number)
                    if current_verse is None:
                        verse_id = insert_verse(book['id'], chapter_id, verse_number)
                        insert_verseversion(verse_id, version, verse_text)
                    else:
                        insert_verseversion(
                            current_verse[0],
                            version,
                            verse_text
                        )
                    
                    print(f"{book[1]} cap {i+1} v. {verse_number} cadastrado!")


if __name__ == '__main__':
    books = get_all_books()  # id, name, abbr, chapters

    get_verses('NTLH', books)
    
    print("Terminado a raspagem de dados!")
