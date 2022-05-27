"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 6/04/2022
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Firefox()


def open_url(abbr, chapter):
    """Open url in browser."""
    driver.get(f"https://pesquisa.biblia.com.br/pt-BR/RA/{abbr}/{chapter}")


def close_driver():
    """Close driver."""
    driver.close()


def click_button(abbr, chapter, verse):
    """Click button in browser."""
    button = driver.find_element(
        By.XPATH, f"//li[@id='{abbr}{chapter}{verse}']/img[1]")
    button.click()
    time.sleep(1)


def get_references(abbr, chapter, verse):
    """Get references in browser."""
    reference = driver.find_element(
        By.XPATH, f"//div[@id='RA{abbr}{chapter}{verse}'][1]")
    time.sleep(2)
    reference.click()
    time.sleep(1)
    references = driver.find_elements(By.CLASS_NAME, "buttonTools")
    for r in references:
        print(r.get_attribute("onclick"))
        #save in database


def get_interlinear(abbr, chapter, verse):
    """Get interlinear."""
    interlinear = driver.find_element(
        By.XPATH, f"//div[@id='RA{abbr}{chapter}{verse}'][2]")
    time.sleep(2)
    interlinear.click()
    time.sleep(1)
    interlineares = driver.find_elements(
        By.XPATH, "//div[@class='toolResult']/ul")
    for i in interlineares:
        print(i.text)
        #save in database


def get_dictionary(abbr, chapter, verse):
    """Get dictionary."""
    dictionary = driver.find_element(
        By.XPATH, f"//div[@id='RA{abbr}{chapter}{verse}'][3]")
    time.sleep(2)
    dictionary.click()
    time.sleep(1)
    dictionaries = driver.find_elements(
        By.XPATH, "//div[@class='toolResult']/ul")
    for d in dictionaries:
        title = d.text.split('-')[0].strip()
        text = ''.join(d.text.split('-')[1:]).strip()
        print(title)
        print(text)
        #save in database


def get_versions(abbr, chapter, verse):
    """Get versions."""
    version = driver.find_element(
        By.XPATH, f"//div[@id='RA{abbr}{chapter}{verse}'][4]")
    time.sleep(2)
    version.click()
    time.sleep(1)
    versions = driver.find_elements(By.XPATH, "//div[@class='toolResult']/ul")        
    for i in range(1, len(versions), 2):
        version = {
            'abbr': versions[i].text.split(' - ')[0],
            'name': versions[i].text.split(' - ')[1],
            'verse': versions[i + 1].text
        }
        print(version['abbr'], end=': ')
        print(version['name'])
        print(version['verse'])
    

#driver.close()
