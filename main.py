from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import datetime


# UNCOMMENT LINES 13-28 TO ACTIVATE WEATHER API
# def format_date_for_api(date_string):
#     try:
#         # Parse the input date in 'YYYY-MM-DD' format
#         parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
#         # Format the date to 'yyyy-M-dTHH:mm:ss'
#         formatted_date = parsed_date.strftime("%Y-%m-%dT%H:%M:%S")
#         return formatted_date
#     except ValueError:
#         raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

# # Example input
# start_travel_date = input("Input the first day of your travel date (YYYY-MM-DD): ")
# final_travel_date = input("Input the last day of your travel date (YYYY-MM-DD): ")

# start_formatted_date = format_date_for_api(start_travel_date)
# final_formatted_date = format_date_for_api(final_travel_date)


# Set up Selenium WebDriver (make sure you have the appropriate driver installed)
service = Service(r'C:\Program Files\chromedriver-win64\chromedriver.exe')    #PASS THE PATH TO CHROMEDRIVER ON YOUR PC
driver = webdriver.Chrome(service=service)
# URL to scrape
url = 'https://en.tengrinews.kz/guide-map/'
driver.get(url)

# Wait for the page to load (you may need to adjust the sleep time)
time.sleep(3)  # Increase if necessary

# Get the page source and parse it
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Find all divs with the class 'map_menu_item_desc'
sights = soup.find_all('div', class_='map_menu_item')
locationsOfSights = soup.find_all('div', class_='map_menu_item_desc')

# Dictionary to store data
sightseeing_data = {}
# Extract name and data_id
for sight in sights:  # assuming you have a list of BeautifulSoup elements as `all_sights`
    name = sight.find('span').text
    data_id = sight.get('data-id')
    
    # Initialize dictionary for each sight with name and data_id
    sightseeing_data[data_id] = {
        'name': name,
        'address': None,  # Placeholder for future data
        'latitude': None,
        'longitude': None,
        'elevation': None,
        'weather': None
    }

for location in locationsOfSights:
    data_id = location.get('data-id')

    # Find all <p> tags within the current location
    paragraphs = location.find_all('p')
        

    # Check each paragraph to see if it contains the keyword "Location:"
    for paragraph in paragraphs:
        if "Location:" in paragraph.text:
            # Extract and clean the address
            address = paragraph.text.replace("Location:", "")
            sightseeing_data[data_id]['address'] = address
            break

        # If no address was found
        if not any("Location:" in p.text for location in locationsOfSights for p in location.find_all('p')):
            sightseeing_data[data_id]['address'] = "Address not found"

# Iterate over a copy of the dictionary keys to avoid issues while deleting
for data_id in list(sightseeing_data.keys()):
    if sightseeing_data[data_id]['name'] == 'Information point Visit Almaty':
        del sightseeing_data[data_id]


load_dotenv()  # take environment variables from .env.

elevation_secret = os.getenv('google_elevation_api')
geocoding_secret = os.getenv('google_geocoding_api')
weather_secret = os.getenv('weather_api')

# Iterate and print only the names
for data_id, details in sightseeing_data.items():
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={details['name']},{'Almaty,Kazakhstan'}&key={geocoding_secret}'
    response = requests.post(geocoding_url)

    # Check the status of the response
    if response.status_code == 200:
        # Parse and print the JSON data if the request was successful
        data = response.json()
    else:
        # Print an error message if the request failed
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response content: {response.text}")
        # Iterate over results
    for result in data['results']:
        # Check if both Almaty and Kazakhstan are present in address components
        found_almaty = False
        found_kazakhstan = False
        for component in result['address_components']:
            if component['long_name'] == 'Almaty':
                found_almaty = True
            if component['long_name'] == 'Kazakhstan':
                found_kazakhstan = True

        # If both Almaty and Kazakhstan are found, extract the coordinates
        if found_almaty or found_kazakhstan:
            sightseeing_data[data_id]['latitude'] = result['geometry']['location']['lat']
            sightseeing_data[data_id]['longitude'] = result['geometry']['location']['lng']


for data_id, details in sightseeing_data.items():
    
    elevation_url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={details['latitude']}%2C{details['longitude']}&key={elevation_secret}'
    response = requests.post(elevation_url)

    # Check the status of the response
    if response.status_code == 200:
        # Parse and print the JSON data if the request was successful
        data = response.json()
        sightseeing_data[data_id]['elevation'] = data['results'][0]['elevation']
    else:
        # Print an error message if the request failed
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response content: {response.text}")

    #UNCOMMENT LINES 141-166 BELOW TO ACTIVATE WEATHER API
    # weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{details['latitude']}%2C{details['longitude']}/{start_travel_date}/{final_travel_date}?unitGroup=metric&key={weather_secret}&contentType=json"
    # response_weather = requests.get(weather_url)
    # if response_weather.status_code == 200:
    #     data_weather = response_weather.json()
        
    #     for day in data_weather['days']:
            
    #         weather_data = [
    #         {
    #             'date': day['datetime'],
    #             'tempmax': day['tempmax'],
    #             'tempmin': day['tempmin'],
    #             'temp': day['temp'],
    #             'humidity': day['humidity'],
    #             'precipprob': day['precipprob'],
    #             'preciptype': day['preciptype'],
    #             'pressure': day['pressure'],
    #             'windspeed': day['windspeed']
    #         }]   

    #         sightseeing_data[data_id][day['datetime']] = weather_data

    # else:
    #     # Print an error message if the request failed
    #     print(f"Request failed with status code: {response_weather.status_code}")
    #     print(f"Response content: {response_weather.text}")

# # Iterate and print the content
# for data_id, details in sightseeing_data.items():
#     print(f"Data ID: {data_id}")
#     for key, value in details.items():
#         print(f"  {key}: {value}")
#     print()  # Just to add a blank line between entries


# Prepare data for DataFrame
output_data = []

#UNCOMMENT LINES THAT ARE DISABLED BELOW FOR WEATHER API
for data_id, details in sightseeing_data.items():
    # for weather in details['weather']: 
        output_data.append({
            'data_id': data_id,
            'name': details['name'],
            'address': details['address'],
            'latitude': details['latitude'],
            'longitude': details['longitude'],
            'elevation': details['elevation'],
            # 'date': weather['date'],
            # 'tempmax': weather['tempmax'],
            # 'tempmin': weather['tempmin'],
            # 'temp': weather['temp'],
            # 'humidity': weather['humidity'],
            # 'precipprob': weather['precipprob'],
            # 'preciptype': weather['preciptype'],
            # 'pressure': weather['pressure'],
            # 'windspeed': weather['windspeed']
        })

# Create DataFrame
df = pd.DataFrame(output_data)

# Save to CSV
df.to_csv('sightseeing_weather_data.csv', index=False)

# Display DataFrame
print(df)