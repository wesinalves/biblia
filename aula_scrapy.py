"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 24/04/2022
"""
import requests, bs4

url_base = 'https://www.bibliaonline.com.br'
res = requests.get(url_base)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
VERSION = 'acf'

books = []
links = soup.select('.jss50 .jss51 a')
for index, link in enumerate(links):
    books.append({'index': index, 'name': link.getText(), 'abbr': link.attrs['href'].split('/')[-1]})

for book in books:
    url = f"{url_base}/{VERSION}/{book['abbr']}"
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    chapters = soup.select('.jss1 a')
    book['number_chapters'] = len(chapters)
    print(f"{book['name']} - {book['number_chapters']}")

number_verses = 0
for book in books:
    for i in range(book['number_chapters']):
        url = f"{url_base}/{VERSION}/{book['abbr']}/{str(i+1)}"
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        verses = soup.select('p')
        number_verses += len(verses)
        for index, verse in enumerate(verses):
            verse_number = len(str(index+1))
            verse_text = verse.getText()[verse_number:].strip()
            with open("biblia.txt" , 'a') as file:
                file.write(f"{book['name']}, {str(i+1)}, {str(index+1)}, {verse_text}\n")
            print(f"{book['name']}, {str(i+1)}, {str(index+1)}, {verse_text}\n")
        
        
