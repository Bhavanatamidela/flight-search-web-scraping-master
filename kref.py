from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import re
import time
import sqlite3

departure= input("Flying from: ")
arrival= input("Flying to: ")
departure_date = input("What date (yyyy-mm-dd): ")
arrival_date=input("What date you will arrive (yyyy-mm-dd):")


def search_flight(from_loc, to_loc, date):

    date = str(date).replace('-', '')

    url = f"https://www.kayak.co.in/flights/{departure}-{arrival}/{departure_date}/{arrival_date}"
    print(f"URL: {url}")
    print("The cheapest flights: \n")

    
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get(url)
    time.sleep(50)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()

    # Getting all the data from the website using html elements and tags.
    airline_name = soup.find_all('span', attrs={'data-test-id': 'airline-name'})
    duration = soup.find_all('span', attrs={'class': 'duration-emphasis'})
    stops = soup.find_all('span', attrs={'class': 'number-stops'})
    depart_times = soup.find_all('span', attrs={'data-test-id': 'departure-time'})
    arrival_times = soup.find_all('span', attrs={'data-test-id': 'arrival-time'})
    price = soup.find_all('span', attrs={'data-test-id': 'listing-price-dollars'})

    # Cleaning up the data, such as getting only text and removing whitespace. This all gets stored in list using list comprehension.
    airlines_name_list = [a.getText().strip() for a in airline_name]
    flight_durations = [b.getText().strip() for b in duration]
    flight_stops = [c.getText().strip() for c in stops]
    depart_list = [d.getText().strip() for d in depart_times]
    arrival_list = [e.getText().strip() for e in arrival_times]
    price_list = [f.getText().strip() for f in price]
    # Removing the euro symbol and commas so data can be converted to int from str
    num_price_list = [int(re.sub('[€,]', '', x)) for x in price_list]

    from_loc_list = [from_loc] * len(num_price_list)
    to_loc_list = [to_loc] * len(num_price_list)
    date_list = [date] * len(num_price_list)

    # Zipping all list together has two benefits, it binds all the data together and type of zip is tuple which is ideal for sqlite
    zipped_list = zip(date_list, from_loc_list, to_loc_list, airlines_name_list, depart_list, arrival_list, flight_durations, flight_stops, num_price_list)

    # connecting to the sql database
    conn = sqlite3.connect("E:/flight-search-web-scraping-master/flight-search-web-scraping-master/Flight-Search/db/flight_search.db")
    c = conn.cursor()

    # Parsing the data
    for data in zipped_list:

        # if the particular flight price is equal to the lowest price returned then print and store the data
        if data[8] == min(num_price_list):
            print(data)
            query = f"INSERT INTO cheap_flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            c.execute(query, data)
            conn.commit()

    conn.close()
  


search_flight(departure,arrival, departure_date)
