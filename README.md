# Almaty Sightseeing Recommendations

This project focuses on scraping sightseeing recommendations in Almaty, a city that has gained increasing popularity among tourists in recent years due to its rich cultural heritage, stunning landscapes, and vibrant atmosphere. Given Almaty's location in a high-elevation region, it is essential to consider the altitude of various tourist spots, as certain areas may not be favorable for individuals with health concerns related to elevation.

### Objective

The main goal of this project is to gather a comprehensive dataset of Almaty's sightseeing spots, including their names, addresses, geographical coordinates (longitude and latitude), elevation, and weather conditions. This data helps create a user-friendly guide for tourists, taking into account health-related factors associated with high-altitude environments.

### Workflow

1. **Web Scraping**: 
   - Using Selenium, scraping sightseeing recommendations for Almaty from a Tengrinews travel guide website.
   - Gather information such as names and addresses of popular sights.

2. **Geolocation Data**: 
   - Use the scraped names to retrieve their corresponding latitude and longitude using the Google Maps Geocoding API.
   
3. **Elevation Information**: 
   - Use the geographic coordinates to query an Google Maps Elevation API and retrieve altitude data for each sightseeing spot.
   - This is particularly important because Almaty is located at a high elevation, with certain areas potentially reaching heights that could pose challenges for those with altitude sensitivities.

4. **Weather Data**: (this part is commented, since exceeding the daily quota for your API usage)
   - Ask for **user input** for the dates of travel, and fetches weather information for these sightseeing spots to give travelers a complete overview of what to expect during their visit. 

5. **Data Output**: 
   - Organize the scraped and retrieved data into a CSV file for easy analysis and visualization.


### Technologies Used

- **Python**: For data processing and automation.
- **Selenium**: For scraping sightseeing data from the web.
- **Google Maps Geogoding API**: To convert scraped addresses into latitude and longitude.
- **Google Maps Elevation API**: For retrieving elevation data based on geographic coordinates.
- **Visual Crossing Weather API**: To retrieve weather forecasts.
- **Pandas**: For organizing and storing the data in CSV format.

### How to Run the Project

1. **Clone this repository.**

2. **Install the Required Libraries**: `pip install -r requirements.txt`

3. **Download ChromeDriver**:
    - Visit [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) to download the correct version for your browser.
  
5. **Set Path to ChromeDriver**:
    - Ensure that the path to the ChromeDriver is correctly specified in the script:
      ```python
      from selenium import webdriver
      
      # Set the path to the ChromeDriver
      driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
      ```

5. **Running the Code**:
    - Execute the script to begin scraping sightseeing recommendations from the website.
    - The data will be processed and stored in a CSV file, including the name, address, coordinates, elevation, and weather forecast for each location.

---

Let me know if you need further details or edits!