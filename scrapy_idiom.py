"""
Script for scraping the Bible from the web.

Source url: bibliaonline.com
Author: Wesin Alves
Data: 2/06/2022
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
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


def save_idioms():
    """Save idioms on database."""
    idioms = driver.find_elements(By.XPATH, "//div[@class='MuiDialog-container MuiDialog-scrollPaper']/div/ul/div")
    length = len(idioms)
    indexes = []
    for idiom in idioms:
        idiom_id = insert_idiom(idiom.text)
        print(idiom.text)
        indexes.append(idiom_id)

    return length, indexes


def get_versions_length(lenght, indexes):
    """Get versions lenght to iterate over."""
    versions_length = []
    for i in range(lenght):
        idiom = driver.find_element(By.XPATH, f"//div[@class='MuiDialog-container MuiDialog-scrollPaper']/div/ul/div[{i+1}]")        
        print(idiom.text)
        idiom.click()
        versions = driver.find_elements(By.XPATH, "//div[@class='MuiDialog-container MuiDialog-scrollPaper']/div/ul/div")
        versions_length.append(len(versions))
        close_dialog()
        click_menu_button()
        click_bibles_button()

    return versions_length


def save_versions(indexes, versions_length):
    """Save versions on database."""
    for key, value in enumerate(versions_length):
        for index in range(value):
            idiom = driver.find_element(By.XPATH, f"//div[@class='MuiDialog-container MuiDialog-scrollPaper']/div/ul/div[{key+1}]")
            idiom.click()
            time.sleep(1)
            version = driver.find_element(By.XPATH, f"//div[@class='MuiDialog-container MuiDialog-scrollPaper']/div/ul/div[{index+1}]")
            name = version.text.replace("'", "''")
            version.click()
            time.sleep(1)
            abbr = driver.current_url.split("/")[-1]
            version_fields = {
                "name": name,
                "abbr": abbr,
            }
            print(version_fields)
            insert_only_version(version_fields, indexes[key])
            time.sleep(1)
            click_menu_button()
            click_bibles_button()


def close_dialog():
    """Close dialog."""
    close = driver.find_element(By.XPATH, "//div[@class='MuiDialogActions-root MuiDialogActions-spacing']/button")
    close.click()


if __name__ == "__main__":
    open_url()
    click_menu_button()
    click_bibles_button()    
    length, indexes = save_idioms()
    versions_lenght = get_versions_length(length, indexes)
    save_versions(indexes, versions_lenght)
