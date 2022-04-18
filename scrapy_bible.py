"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 6/04/2022
"""

import requests, bs4
from database import insert_book, insert_chapter, insert_verse

url_base = 'https://www.bibliaonline.com.br'
res = requests.get(url_base)
soup = bs4.BeautifulSoup(res.text, 'html.parser')

# get versions
print("Iniciando a raspagem de dados!")

# get books
books = []
books_link = soup.select('.jss50 .jss51 a')
for index, book in enumerate(books_link):    
    books.append({'index': index, 'name': book.getText(), 'abbr': book.attrs['href'].split('/')[-1]})

# get chapters
for book in books:
    url = url_base + '/ara' + '/' + book['abbr']    
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    chapters = soup.select('.jss1 a')
    book['number_chapters'] = len(chapters)        
    book['id'] = insert_book(book['name'], book['abbr'], book['number_chapters'])    


#print(books[0])
# get verses
number_verses = 0
VERSION_ID = 1
for book in books:
    for i in range(book['number_chapters']):
        url = url_base + '/ara' + '/' + book['abbr'] + '/' + str(i+1)
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        verses = soup.select('p')
        number_verses += len(verses)
        chapter_id = insert_chapter(book['id'], i+1, str(len(verses)))
        for index, verse in enumerate(verses):
            if verse.attrs['class'][0] == 'MuiTypography-root':
                break
            verse_number = len(str(index + 1))
            verse_text = verse.getText()[verse_number:].strip()
            verse_id = insert_verse(book['id'], chapter_id, VERSION_ID, index+1, verse_text)
            print(f"{book['name']} cap {i+1} v. {index + 1} cadastrado!")
        

print("Terminado a raspagem de dados!")