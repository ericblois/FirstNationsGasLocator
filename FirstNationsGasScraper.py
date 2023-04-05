from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import string
# Import regex
import re

#Set options for driver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

#Start driver using preset options
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.implicitly_wait(10)

# Cities to search for within a radius of 200km
key_cities = [
    "London, Ontario",
    "Toronto, Ontario",
    "Ottawa, Ontario",
    "Barrie, Ontario",
    "Peterborough, Ontario",
    "Kingston, Ontario",
    "Bancroft, Ontario",
    "Whitney, Ontario",
    "Parry Sound, Ontario",
    "North Bay, Ontario",
    "Sudbury, Ontario",
    "Blind River, Ontario",
    "Temagami, Ontario",
    "Chapleau, Ontario",
    "Timmins, Ontario",
    "Marathon, Ontario",
    "Hearst, Ontario",
    "Abitibi Canyon, Ontario",
    "Moose River, Ontario",
    "Geraldton, Ontario",
    "Thunder Bay, Ontario",
    "Ignace, Ontario",
    "Mine Centre, Ontario",
    "Kenora, Ontario",
    "Winnipeg, Manitoba",
    "Brandon, Manitoba",
    "Moosomin, Saskatchewan",
    "Swan River, Manitoba",
    "Overflowing River, Manitoba",
    "Saint Martin, Manitoba",
    "Grand Rapids, Manitoba",
    "Yorkton, Saskatchewan",
    "Regina, Saskatchewan",
    "Saskatoon, Saskatchewan",
    "Nipawin, Saskatchewan",
    "Green Lake, Saskatchewan",
    "Flin Flon, Manitoba",
    "Lloydminster, Saskatchewan",
    "Swift Current, Saskatchewan",
    "Medicine Hat, Alberta",
    "Calgary, Alberta",
    "Edmonton, Alberta",
    "Buffalo Narrows, Saskatchewan",
    "Fort McMurray, Alberta",
    "Wandering River, Alberta",
    "High Prairie, Alberta",
    "Red Deer, Alberta",
    "Hinton, Alberta",
    "Macklin, Saskatchewan",
    "Golden, British Columbia",
    "Kelowna, British Columbia",
    "Creston, British Columbia",
    "Fort Macleod, Alberta",
    "Whistler, British Columbia",
    "Vancouver, British Columbia",
    "Campbell River, British Columbia",
    "Port McNeill, British Columbia",
    "Blue River, British Columbia",
    "Williams Lake, British Columbia",
    "Fort St. John, British Columbia",
    "Prince George, British Columbia",
    "Houston, British Columbia",
    "Prince Rupert, British Columbia",
    "Montreal, Quebec",
    "Quebec City, Quebec",
    "Mont Laurier, Quebec",
    "Dorval-Lodge, Quebec",
    "Malartic, Quebec",
    "Trois Rivieres, Quebec",
    "La Tuque, Quebec",
    "Saguenay, Quebec",
    "Edmundston, New Brunswick",
    "Amqui, Quebec",
    "Gaspe, Quebec",
    "Fredericton, New Brunswick",
    "Moncton, New Brunswick",
    "Bathurst, New Brunswick",
    "Lunenburg, Nova Scotia",
    "Antigonish, Nova Scotia",
    "Stephenville, Newfoundland",
    "Deer Lake, Newfoundland",
    "Grand Falls-Windsor, Newfoundland",
    "Clarenville, Newfoundland",
    "St. John's, Newfoundland"
]

ALL_HREFS = {}

urls = pd.read_csv("links.csv")
for url in urls["Link"]:
    ALL_HREFS[url] = True

#driver.get("https://firstnationsgas.ca/search/")

def get_all_hrefs():
    for city in key_cities:
        print('\033[37m' + f"Searching 200km around {city}...")
        get_hrefs(city)

def get_hrefs(city):
    driver.get("https://firstnationsgas.ca/search/")
    radius = Select(driver.find_element(By.ID, "toolset-maps-distance-radius"))
    radius.select_by_value("200")
    searchbar = driver.find_element(By.ID, "toolset-maps-distance-center")
    searchbar.send_keys(city)
    searchbar.send_keys(Keys.RETURN)
    # Check if multiple pages
    next = 1
    count = 1
    while next is not None:
        try:
            table = driver.find_element(By.ID, "station-table").find_element(By.TAG_NAME, "tbody")
            print('\033[37m' + f"Collecting new stations from page {count}...")
            dup_count = 0
            for table_row in table.find_elements(By.TAG_NAME, "tr"):
                tds = table_row.find_elements(By.TAG_NAME, "td")
                link = tds[1].find_element(By.TAG_NAME, "a").get_attribute("href")
                if ALL_HREFS.get(link) is None:
                    ALL_HREFS[link] = True
                    print('\033[92m' + link)
                else:
                    dup_count += 1
            print('\033[91m' + f"Found {dup_count} duplicates.")
            count += 1
            pagination = driver.find_element(By.ID, "pagination-buttons")
            next = pagination.find_elements(By.TAG_NAME, "a")[-1]
            if next.text == "NEXT":
                next.click()
            else:
                next = None
        except:
            next = None

def get_station_info(url):
    print('\033[37m' + f"Getting station info from {url}...")
    driver.get(url)
    content = driver.find_element(By.CLASS_NAME, "entry-content")
    # Name
    name = content.find_element(By.TAG_NAME, "h1").text
    # Address, Phone, Band
    contact = content.find_element(By.ID, 'contact').find_element(By.XPATH, "./..").find_elements(By.TAG_NAME, "p")[0:2]
    contact_info = contact[0].text.splitlines()
    address = ""
    phone = ""
    email = ""
    for line in contact_info:
        words = line.split(' ')
        if words[0] == "Address:":
            address = ' '.join(words[1:])
        elif words[0] == "Phone:":
            phone = ' '.join(words[1:])
        elif words[0] == "Email:":
            email = words[1]
    try:
        band = contact[1].text
    except:
        band = ""
    # Features, Serves
    details_lines = content.find_element(By.ID, 'details').text.splitlines()
    features = ""
    serves = ""
    for i, line in enumerate(details_lines):
        if line == "Features" and details_lines[i+1] != "Serves":
            features = details_lines[i+1]
        elif line == "Serves" and details_lines[i+1] != "Station Map" and details_lines[i+1] != "View station on other sites":
            serves = details_lines[i+1]
    # Separate address into street address, city, province, postal code
    if address == "":
        street_address = ''
        city = ''
        province = ''
        postal_code = ''
    else:
        addr_parts = re.split(r'[,\ ]{2}', address)
        if addr_parts[len(addr_parts) - 1] == "Canada" and addr_parts[len(addr_parts) - 2] == "Canada":
            # Address is in format: Street address, City, Province Postal Code
            street_address = addr_parts[0]
            city = addr_parts[1]
            prov_post = addr_parts[2]
            prov_post = prov_post.split(' ')
            province = prov_post[0]
            postal_code = ''.join(prov_post[1:])
        elif addr_parts[len(addr_parts) - 2] == "Canada":
            # Address is in format: Postal Code, City, Province
            postal_code = addr_parts[0]
            city = addr_parts[1]
            province = addr_parts[2]
            street_address = ''
        elif len(addr_parts[len(addr_parts) - 1].split(' ')) == 3:
            # Address is in format: 123 Main St, City, Province Postal Code
            street_address = addr_parts[0]
            city = addr_parts[1]
            prov_post = addr_parts[2]
            prov_post = prov_post.split(' ')
            province = prov_post[0]
            postal_code = ''.join(prov_post[1:])
        elif len(addr_parts[len(addr_parts) - 1]) < 3:
            # Address is in format: 123 Main St, City, Province
            street_address = addr_parts[0]
            city = addr_parts[1]
            province = addr_parts[2]
            postal_code = ''
        else:
            # Address is in format: 123 Main St, City, Province Postal Code, Country
            street_address = addr_parts[len(addr_parts) - 4]
            city = addr_parts[len(addr_parts) - 3]
            prov_post = addr_parts[len(addr_parts) - 2]
            prov_post = prov_post.split(' ')
            province = prov_post[0]
            postal_code = ''.join(prov_post[1:])
    print('\033[92m' + f"Found info: {[name, phone, email, band, street_address, city, province, postal_code, features, serves]}")
    #print([name, phone, email, band, street_address, city, province, postal_code, features, serves])
    return [name, phone, email, band, street_address, city, province, postal_code, features, serves]

def get_all_info():
    stations = []
    for href in ALL_HREFS.keys():
        stations.append(get_station_info(href))
    return pd.DataFrame(stations, columns=['Name', 'Phone', 'Email', 'Band', 'Street Address', 'City', 'Province', 'Postal Code', 'Features', 'Serves'])

#get_all_hrefs()
#links = list(ALL_HREFS.keys())
#link_df = pd.DataFrame(links, columns=['Link'])
#link_df.to_csv("links.csv", index=False)
#print(ALL_HREFS)
#get_station_info('https://firstnationsgas.ca/station/gen7-fuel-moravian/')
#get_hrefs("Yorkton, Saskatchewan")
stations = get_all_info()
stations.to_csv("stations.csv", index=False)
print("done")