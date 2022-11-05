"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 6/04/2022
"""

from database import get_all_books, get_chapters_by_book
from extract import extract_references, extract_interlinear, extract_dictionary


books = get_all_books()  # id, name, abbr, chapters


for b in range(47, len(books)):
    print(f'scrapying {books[b][1]}', end='', flush=True)
    chapters = get_chapters_by_book(books[b][0])  # id, cap, vers, livro
    for i in range(0, len(chapters)):
        print('.', end='', flush=True)
        for verse in range(1, chapters[i][2] + 1):
            extract_references(books[b][2], chapters[i][1], verse)
            extract_interlinear(books[b][2], chapters[i][1], verse)
            extract_dictionary(books[b][2], chapters[i][1], verse)
    print('')    
