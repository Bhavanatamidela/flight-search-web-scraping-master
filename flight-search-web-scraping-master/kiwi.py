from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time
import sqlite3

from_loc= input("Flying from: ")
to_loc= input("Flying to: ")
departure_date = input("What date (yyyy-mm-dd): ")
arrival_date=input("What date you will arrive (yyyy-mm-dd):")


def search_flight(from_loc, to_loc, departure_date, arrival_date):

    url = f"https://www.kiwi.com/en/search/results/{from_loc}-india/{to_loc}-india/{departure_date}/{arrival_date}"
            
    print(f"URL: {url}")
    print("The cheapest flights: \n")

    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    

    driver.quit()
    # Getting all the data from the website using html elements and tags.
    airline_name = soup.find_all('img', attrs={'class': 'CarrierLogo__StyledImage-sc-1rhi78a-0 hLDGBn'})
    airline_lists = []
    for val in airline_name:
        airline_lists.append(val["title"])
    #duration = soup.find_all('div', attrs={'class': 'leg-info__duration__value'})
    #stops = soup.find_all('div', attrs={'class': 'leg-info__stops'})
    #depart_times = soup.find_all('div', attrs={'class': 'leg-info__times__item--departure'})
    #arrival_times = soup.find_all('div', attrs={'class': 'leg-info__times__item--arrival'})
    #price = soup.find_all('div', attrs={'class': 'price-value'})
    print(airline_lists)

    # Cleaning up the data, such as getting only text and removing whitespace. This all gets stored in a list using list comprehension.
    #airlines_name_list = [a.getText().strip() for a in airline_name]
    #flight_durations = [b.getText().strip() for b in duration]
    #flight_stops = [c.getText().strip() for c in stops]
    #depart_list = [d.find('span', attrs={'class': 'times__item-value'}).getText().strip() for d in depart_times]
    #arrival_list = [e.find('span', attrs={'class': 'times__item-value'}).getText().strip() for e in arrival_times]
    #price_list = [f.getText().strip() for f in price]

   # print(airlines_name_list)
    #print(flight_durations)
    #print(flight_stops)
    #print(depart_list)
    #print(arrival_list)
    #print(price_list)
    # Removing the currency symbol and commas so data can be converted to int from str
    num_price_list = [int(re.sub('[^0-9]', '', x)) for x in price_list]

    from_loc_list = [from_loc] * len(num_price_list)
    to_loc_list = [to_loc] * len(num_price_list)

    # Zipping all list together has two benefits, it binds all the data together and type of zip is tuple which is ideal for sqlite
    zipped_list = zip(from_loc_list, to_loc_list, airlines_name_list, depart_list, arrival_list, flight_durations, flight_stops, num_price_list, [departure_date]*len(num_price_list), [arrival_date]*len(num_price_list))

    # Connecting to the sql database
    conn = sqlite3.connect('E:/flight-search-web-scraping-master/flight-search-web-scraping-master/Flight-Search/db/flight_search.db')
    c = conn.cursor()
    # Creating table
    c.execute('''CREATE TABLE IF NOT EXISTS flights (from_loc TEXT, to_loc TEXT, airline_name TEXT, depart_time TEXT, arrival_time TEXT, duration TEXT, stops TEXT, price INTEGER, departure_date TEXT, arrival_date TEXT)''')

    c.executemany('''INSERT INTO flights (from_loc, to_loc, airline_name, depart_time, arrival_time, duration, stops, price, departure_date, arrival_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', zipped_list)

    conn.commit()
    conn.close()
    print("Data inserted into database.")
search_flight(from_loc, to_loc, departure_date, arrival_date)
    
