from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import bs4
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from database import get_books, get_chapters


books = get_books()

for book in books:
    chapters = get_chapters(book[0]) # id, cap, vers, livro
    for chapter in chapters:
        print(chapter)
        break
    break

