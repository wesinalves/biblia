from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import bs4
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Firefox()


def open_url(abbr, chapter):
    """Open url in browser"""    
    driver.get(f"https://pesquisa.biblia.com.br/pt-BR/RA/{abbr}/{chapter}")    


def click_button(abbr, chapter, verse):
    """Click button in browser"""
    button = driver.find_element(By.XPATH, f"//li[@id='{abbr}{chapter}{verse}']/img[1]")
    button.click()
    time.sleep(1)


# get references
reference = driver.find_element(By.XPATH, "//div[@id='RAgn11'][1]")
time.sleep(2)
reference.click()
time.sleep(1)
references = driver.find_elements(By.CLASS_NAME, "buttonTools")
for r in references:
    print(r.get_attribute("onclick"))


# get interlinear
interlinear = driver.find_element(By.XPATH, "//div[@id='RAgn11'][2]")
time.sleep(2)
interlinear.click()
time.sleep(1)
interlineares = driver.find_elements(By.XPATH, "//div[@class='toolResult']/ul")
for i in interlineares:
    print(i.text)

# get dictionary
dictionary = driver.find_element(By.XPATH, "//div[@id='RAgn11'][3]")
time.sleep(2)
dictionary.click()
time.sleep(1)
dictionaries = driver.find_elements(By.XPATH, "//div[@class='toolResult']/ul")
for d in dictionaries:
    print(d.text)

# get versões

#driver.close()
