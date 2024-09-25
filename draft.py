# import requests
# import pandas as pd
# from bs4 import BeautifulSoup

# kz_stats_url = "https://simplemaps.com/data/kz-cities"

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# } # as default user agent is disallowed in robots.txt

# response = requests.get(kz_stats_url,headers = headers)

# if (response.status_code != 200):
#     print(f"Failed to get the webpage: {response.status_code}")
        
# soup = BeautifulSoup(response.text, 'html.parser')

# kz_stats = soup.find('table', class_ = 'htCore')

# print(kz_stats)\
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
import os
import requests

# Set up Selenium WebDriver (make sure you have the appropriate driver installed)
service = Service(r'C:\Program Files\chromedriver-win64\chromedriver.exe')    #PASS THE PATH TO CHROMEDRIVER ON YOUR PC
driver = webdriver.Chrome(service=service)
# URL to scrape
url = 'https://simplemaps.com/data/kz-cities'
driver.get(url)

# Wait for the page to load (you may need to adjust the sleep time)
time.sleep(5)  # Increase if necessary

# Get the page source and parse it
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Find the table with the class 'hdCore'
table = soup.find('table', class_='htCore')

city_data = []
if table:
    # Iterate through the rows in the table body
    for row in table.find_all('tr'):
        columns = row.find_all('td')  # Get all columns in the row
        if columns:  # Ensure there are columns
            population = columns[7].text.strip()
            if not population:  # Skip if population is empty
                continue
        
            # Extract the required columns and handle empty values in admin status
            city = columns[0].text.strip()
            lat = columns[1].text.strip()
            lon = columns[2].text.strip()
            region = columns[5].text.strip()
            
            # Fill empty admin status with 'minor'
            admin_status = columns[6].text.strip() or 'minor'

            # Append the cleaned data to the list
            city_info = [city, lat, lon, region, admin_status, population]
            city_data.append(city_info)
            

    print("City Data:")
    for data in city_data:
        print(data)  # Print each row of data
else:
    print("Table with class 'hdCore' not found.")

# Close the driver
driver.quit()

OpenWeather_API = "5e022d8a933f8e8aa245bbc570702861"

# # Load environment variables from the .env file
# load_dotenv()

# # Access the API key
# OpenWeather_API = os.getenv('API_KEY')

lat = 50.3500
lon = 83.5167
date = '2024-01-01'
unix_timestamp = int(time.mktime(time.strptime(date, '%Y-%m-%d')))
url_open_weater = f'https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&date={unix_timestamp}&units=metric&appid={OpenWeather_API}'

response = requests.get(url)
if response.status_code == 200:
    try:
        data = response.json()
        print(data)
    except ValueError:
        print("Response content is not valid JSON")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(f"Response content: {response.text}")
