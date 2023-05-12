"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 6/04/2022
"""

import requests, bs4
from database import get_verse, insert_chapter, insert_verseversion,\
    insert_verse, get_chapter, get_all_books, get_chapters_by_book

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
            url = f"{url_base}/{version}/{book[2]}/{str(i+1)}"
            print(url)
            res = requests.get(url, verify=False)
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            verses = soup.select(".versiculoTexto")
            number_verses += len(verses)
            chapter = get_chapter(book[0], i+1)
            
            chapter_id = chapter[0]

            # verses % 10
            # # ?page={page + 1}
            
            for index, verse in enumerate(verses):                
                
                verse_number = len(str(index + 1))
                verse_text = verse.getText()[verse_number:].strip().replace(
                    "'", "''")
                current_verse = get_verse(book[0], chapter_id, index+1)
                # if current_verse is None:
                #     verse_id = insert_verse(book['id'], chapter_id, index+1)
                #     insert_verseversion(verse_id, version[0], verse_text)
                # else:
                #     insert_verseversion(
                #         current_verse[0],
                #         version[0],
                #         verse_text
                #     )
                
                print(f"{book[1]} cap {i+1} v. {index + 1} cadastrado!")


if __name__ == '__main__':
    books = get_all_books()  # id, name, abbr, chapters

    get_verses('NTLH', books)
    
    print("Terminado a raspagem de dados!")
