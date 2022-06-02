"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 2/06/2022
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from database import insert_idiom, insert_only_version


driver = webdriver.Firefox()

def open_url():
    """Open url in browser."""
    driver.get("https://www.bibliaonline.com.br")

def close_driver():
    """Close driver."""
    driver.close()


def click_menu_button():
    """Click menu button in browser."""
    button = driver.find_element(
        By.XPATH, "//div[@class='jss15']/a")
    button.click()
    time.sleep(1)


def click_bibles_button():
    """Click bibles button in menu."""
    button = driver.find_element(
        By.XPATH, "//div[@id='menu']/div[3]/ul/li[3]")    
    button.click()
    time.sleep(1)

def get_idiom():
    idioms = driver.find_elements(By.XPATH, "//div[@class='MuiDialog-container MuiDialog-scrollPaper']/div/ul/div")
    idioms[0].click()  
    time.sleep(1)



def close_button():
    pass

def get_versions():
    pass


if __name__ == "__main__":
    open_url()
    click_menu_button()
    click_bibles_button()
    get_idiom()