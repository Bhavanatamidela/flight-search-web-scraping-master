from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import re
import time
import sqlite3

from_loc= input("Flying from: ")
to_loc= input("Flying to: ")
departure_date = input("What date (yyyy-mm-dd): ")
arrival_date=input("What date you will arrive (yyyy-mm-dd):")


def search_flight(from_loc, to_loc, departure_date, arrival_date):

    url = f"https://www.kayak.com/flights/{from_loc}-{to_loc}/{departure_date}/{arrival_date}"
    print(f"URL: {url}")
    print("The cheapest flights: \n")

    driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()))
    driver.get(url)
    time.sleep(30)
    soup = BeautifulSoup(driver.page_source, 'lxml')
   
    driver.quit()

    # Getting all the data from the website using html elements and tags.
    airline_name = soup.find_all('div', attrs={'class': 'section duration allow-multi-modal-icons'})
    duration = soup.find_all('div', attrs={'class': 'section duration allow-multi-modal-icons'})
    stops = soup.find_all('div', attrs={'class': 'section stops'})
    depart_times = soup.find_all('div', attrs={'class': 'section times'})
    arrival_times = soup.find_all('div', attrs={'class': 'section times'})
    price = soup.find_all('div', attrs={'class': 'section price-section'})

    # Cleaning up the data, such as getting only text and removing whitespace. This all gets stored in a list using list comprehension.
    airlines_name_list = [a.find('span', attrs={'class': 'codeshares-airline-names'}).getText().strip() for a in airline_name]
    flight_durations = [b.find('span', attrs={'class': 'duration'}).getText().strip() for b in duration]
    flight_stops = [c.find('div', attrs={'class': 'stops-text'}).getText().strip() for c in stops]
    depart_list = [d.find_all('span', attrs={'class': 'time-2'})[0].getText().strip() for d in depart_times]
    arrival_list = [e.find_all('span', attrs={'class': 'time-2'})[1].getText().strip() for e in arrival_times]
    price_list = [f.find('span', attrs={'class': 'price-text'}).getText().strip() for f in price]
    # Removing the dollar sign and commas so data can be converted to int from str
    num_price_list = [int(re.sub('[$,]', '', x)) for x in price_list]

    from_loc_list = [from_loc] * len(num_price_list)
    to_loc_list = [to_loc] * len(num_price_list)
    departure_date_list = [departure_date] * len(num_price_list)
    arrival_date_list = [arrival_date] * len(num_price_list)

    # Zipping all list together has two benefits, it binds all the data together and type of zip is tuple which is ideal for sqlite
    zipped_list = zip(departure_date_list, from_loc_list, to_loc_list, airlines_name_list, depart_list, arrival_list, flight_durations, flight_stops, num_price_list, arrival_date_list)

    # Connecting to the sql database
    conn = sqlite3.connect('E:/flight-search-web-scraping-master/flight-search-web-scraping-master/Flight-Search/db/flight_search.db')
    c = conn.cursor()
    
    c.execute('CREATE TABLE IF NOT EXISTS flights_data (id INTEGER PRIMARY KEY, from_loc TEXT, to_loc TEXT, airline TEXT, depart_time TEXT, arrival_time TEXT, duration TEXT, stops TEXT, price INTEGER, departure_date TEXT, arrival_date TEXT)')

    # Insert parsed data into SQLite table
    for i in range(len(airlines_name_list)):
        values = (from_loc, to_loc, airlines_name_list[i], depart_list[i], arrival_list[i], flight_durations[i], flight_stops[i], num_price_list[i], departure_date, arrival_date)
        c.execute('INSERT INTO flights_data (from_loc, to_loc, airline, depart_time, arrival_time, duration, stops, price, departure_date, arrival_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)
       

    conn.commit()
    conn.close()
    
    print("Data inserted into database.")
search_flight(from_loc, to_loc, departure_date, arrival_date)
