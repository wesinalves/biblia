"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 6/04/2022
"""

import time
from database import get_books, get_chapters
from navigation import get_versions, open_url, close_driver,\
    click_button, get_references, get_interlinear, get_dictionary


books = get_books()  # id, name, abbr, chapters

for book in books:
    chapters = get_chapters(book[0])  # id, cap, vers, livro     
    for chapter in chapters:        
        print(chapter)
        open_url(book[2], chapter[1])
        for verse in range(1, chapter[2]):
            click_button(book[2], chapter[1], verse)
            #get_references(book[2], chapter[1], verse)
            #get_interlinear(book[2], chapter[1], verse)
            #get_dictionary(book[2], chapter[1], verse)
            get_versions(book[2], chapter[1], verse)
            close_driver()
            time.sleep(1)
            break
        break
    break
