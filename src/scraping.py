import random
from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

import warnings
warnings.filterwarnings('ignore')

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
opciones= Options()
opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
opciones.add_argument('--start-maximized')
opciones.add_argument('user.data-dir=selenium')
opciones.add_argument('--incognito')

contador = 0
def civitatiScrape():
    """
    Scrapes all the reviews of the civitatis' freetour 
    in Barcelona and saves them as a html file.
    Methods:
        random + sleep: random and time libraries had been combined to generate 
                        aleatory waiting times between actions, as setting a fixed 
                        lenght will make the server to recognize the robot and expell it.
        ActionChains: directly clicking on the 'next button' to pursue the scraping will 
                      automatically cause the expulsion from the server. In order 
                      to avoid honey pots and better fake human behaviour, this action 
                      has been divided in several steps.
    Return:
        - If the bot is expelled from the server, it returns the number 
        of web pages that where scraped, so the scraping can continue from 
        that point if desired. It will also return the document in which the 
        reviews were saved and will close the driver.
        - If the scraping reaches the last possible url, it returns how many 
        web pages were scraped and the document in which the reviews had been saved. 
        It will also close the driver.
    """
    revius = open("civitatis.html", "a", encoding='utf-8')
    try:
        global contador    
        contador += 1
        espera = round(random.uniform(3, 6),2)
        sleep(espera)
        resultado = driver.find_element_by_css_selector('#comments-id-duplicado > div')
        with open("civitatis.html", "a", encoding='utf-8') as file:
            file.write(resultado.text + '\n')
    except:
        return print(f'Se paró en la página {contador}'), revius, driver.quit()

    try:
        espera = round(random.uniform(3, 6),2)
        sleep(espera)
        action = ActionChains(driver)
        m = driver.find_element_by_css_selector("#comments-id-duplicado > div > nav > div.right.--no-icon > a.next-element")
        actions = ActionChains(driver)
        actions.move_to_element(m)
        actions.click(m)
        actions.perform()    
        return civitatiScrape()
    except:
        return print(f'Terminado. {contador} páginas fueron visitadas'), revius, driver.quit()