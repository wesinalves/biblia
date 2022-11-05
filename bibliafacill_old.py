"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 6/04/2022
"""

import time
from database import get_all_books, get_chapters_by_book
from navigation import get_versions, open_url, close_driver,\
    click_button, get_references, get_interlinear, get_dictionary, scroll_page


books = get_all_books()  # id, name, abbr, chapters

for book in books:
    print(f'scrapying {book[1]}...')
    chapters = get_chapters_by_book(book[0])  # id, cap, vers, livro     
    for i in range(35, len(chapters)):
        open_url(book[2], chapters[i][1])
        for verse in range(1, chapters[i][2]):
            click_button(book[2], chapters[i][1], verse)
            get_references(book[2], chapters[i][1], verse)
            get_interlinear(book[2], chapters[i][1], verse)
            get_dictionary(book[2], chapters[i][1], verse)
            if verse % 10 == 0:
                scroll_page()
                scroll_page()
            time.sleep(1)
    break

close_driver()
