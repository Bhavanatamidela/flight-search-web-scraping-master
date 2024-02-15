from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import re
import time
import sqlite3

from_loc = input("Flying from: ")
to_loc = input("Flying to: ")
date = input("What date (dd/mm/yyyy): ")


    
url = f"https://www.cleartrip.com/flights/results?from={from_loc}&to={to_loc}&depart_date={date}&adults=1&childs=0&infants=0&class=Economy&airline=&carrier=&intl=n&sd=&ed=&view_name=normal&time=anytime&sort=price_a"
print(f"URL: {url}")
print("The cheapest flights: \n")




from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time
import sqlite3

 driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(30)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()