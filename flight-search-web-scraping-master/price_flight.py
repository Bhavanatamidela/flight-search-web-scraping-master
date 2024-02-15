from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import re
import time
import sqlite3

from_loc = input("Flying from: ")
to_loc = input("Flying to: ")
date = input("What date (yyyy-mm-dd): ")

def search_flight(from_loc, to_loc, date):
    
    url = f"https://www.google.com/flights?hl=en#flt={from_loc}.{to_loc}.{date};c:INR;e:1;sd:1;t:f"
    print(f"URL: {url}")
    print("The cheapest flights: \n")

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get(url)
    time.sleep(50)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()

    # Getting all the data from the website using html elements and tags.
    airline_name = soup.find_all('div', attrs={'class': 'gws-flights-results__itinerary-card-header-airline'})
    duration = soup.find_all('div', attrs={'class': 'gws-flights-results__duration'})
    stops = soup.find_all('div', attrs={'class': 'gws-flights-results__stops'})
    depart_times = soup.find_all('div', attrs={'class': 'gws-flights-results__times'})
    price = soup.find_all('div', attrs={'class': 'gws-flights-results__price'})

    # Cleaning up the data, such as getting only text and removing whitespace. This all gets stored in list using list comprehension.
    airlines_name_list = [a.getText().strip() for a in airline_name]
    flight_durations = [b.getText().strip() for b in duration]
    flight_stops = [c.getText().strip() for c in stops]
    depart_list = [d.getText().strip() for d in depart_times]
    price_list = [f.getText().strip() for f in price]
    # Removing the currency symbol and commas so data can be converted to int from str
    num_price_list = [int(re.sub('[^0-9]', '', x)) for x in price_list]

    from_loc_list = [from_loc] * len(num_price_list)
    to_loc_list = [to_loc] * len(num_price_list)
    date_list = [date] * len(num_price_list)

    # Zipping all list together has two benefits, it binds all the data together and type of zip is tuple which is ideal for sqlite
    zipped_list = zip(date_list, from_loc_list, to_loc_list, airlines_name_list, depart_list, flight_durations, flight_stops, num_price_list)

    # connecting to the sql database
    conn = sqlite3.connect("flight_search.db")
    c = conn.cursor()

    # Creating the 'cheap_flights' table if it does not already exist
    c.execute('''CREATE TABLE IF NOT EXISTS cheap_flights
                 (Date text, From_Location text, To_Location text, Airline text, Depart_Time text, Duration text, Stops text, Price int)''')

    # Parsing the data
    for data in zipped_list:

        # if the particular flight price is equal to the lowest price returned then print and store the data
        if data[7] == min(num_price_list):
            print(data)
            c.execute("INSERT INTO cheap_flights VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)

    conn.commit()
    conn.close()
    
 
search_flight(from_loc, to_loc, date)