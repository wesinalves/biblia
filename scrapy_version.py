"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 6/04/2022
"""

import requests, bs4
from database import get_verse, insert_chapter, insert_verseversion,\
    insert_verse, get_chapter, get_version, get_all_books

"""Setup initial parameters."""
url_base = 'https://www.bibliaonline.com.br'
res = requests.get(url_base)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
print("Iniciando a raspagem de dados!")


def get_verses(version, books):
    """Get verses."""
    number_verses = 0
    for book in books:
        for i in range(book[3]):
            url = f"{url_base}/\
                {version[2]}/{book[2]}/{str(i+1)}"
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            verses = soup.select('p')
            number_verses += len(verses)
            chapter = get_chapter(book[0], i+1)
            if chapter is None:
                chapter_id = insert_chapter(book[0], i+1, str(len(verses)))
            else:
                chapter_id = chapter[0]
            
            for index, verse in enumerate(verses):
                try:
                    if verse.attrs['class'][0] == 'MuiTypography-root':
                        break
                    verse_number = len(str(index + 1))
                    verse_text = verse.getText()[verse_number:].strip().replace(
                        "'", "''")
                    current_verse = get_verse(book[0], chapter_id, index+1)
                    if current_verse is None:
                        verse_id = insert_verse(book[0], chapter_id, index+1)
                        insert_verseversion(verse_id, version[0], verse_text)
                    else:
                        insert_verseversion(
                            current_verse[0],
                            version[0],
                            verse_text
                        )
                    
                    print(f"{book[1]} cap {i+1} v. {index + 1} cadastrado!")
                except:
                    print(f'Não foi possível completar a raspagem do livro {book[1]} cap. {i+1} verso {index + 1}')


if __name__ == '__main__':    

    books = get_all_books()  
    
    for i in range(140, 160):        
        version = get_version(i)
        get_verses(version, books)
        print(f"Terminado a raspagem de dados i = {i}!")
