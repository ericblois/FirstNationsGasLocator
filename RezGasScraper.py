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
#driver = webdriver.Chrome("/Applications/chromedriver", options=chrome_options)
driver.implicitly_wait(10)

area_urls = [
    "https://www.rezgas.com/results.php?area=ab_north",
    "https://www.rezgas.com/results.php?area=ab_Ecentral",
    "https://www.rezgas.com/results.php?area=ab_Wcentral",
    "https://www.rezgas.com/results.php?area=ab_edmonton",
    "https://www.rezgas.com/results.php?area=ab_calgary",
    "https://www.rezgas.com/results.php?area=ab_south",
    "https://www.rezgas.com/results.php?area=rockies",
    "https://www.rezgas.com/results.php?area=klemtu",
    "https://www.rezgas.com/results.php?area=bella",
    "https://www.rezgas.com/results.php?area=alexis",
    "https://www.rezgas.com/results.php?area=williams_lake",
    "https://www.rezgas.com/results.php?area=quesnel",
    "https://www.rezgas.com/results.php?area=charlotte",
    "https://www.rezgas.com/results.php?area=rupert",
    "https://www.rezgas.com/results.php?area=hazelton",
    "https://www.rezgas.com/results.php?area=burns_lake",
    "https://www.rezgas.com/results.php?area=P_George",
    "https://www.rezgas.com/results.php?area=mc_leod",
    "https://www.rezgas.com/results.php?area=dawson_creek",
    "https://www.rezgas.com/results.php?area=mackenzie",
    "https://www.rezgas.com/results.php?area=ft_nelson",
    "https://www.rezgas.com/results.php?area=good_hope",
    "https://www.rezgas.com/results.php?area=hope_cache",
    "https://www.rezgas.com/results.php?area=penticton",
    "https://www.rezgas.com/results.php?area=merritt",
    "https://www.rezgas.com/results.php?area=cache",
    "https://www.rezgas.com/results.php?area=kamloops",
    "https://www.rezgas.com/results.php?area=salmon_arm",
    "https://www.rezgas.com/results.php?area=vernon",
    "https://www.rezgas.com/results.php?area=kelowna",
    "https://www.rezgas.com/results.php?area=hwy99",
    "https://www.rezgas.com/results.php?area=YVR_east",
    "https://www.rezgas.com/results.php?area=gvrd",
    "https://www.rezgas.com/results.php?area=ISL_north",
    "https://www.rezgas.com/results.php?area=ISL_central",
    "https://www.rezgas.com/results.php?area=ISL_PacRim",
    "https://www.rezgas.com/results.php?area=ISL_cowichan",
    "https://www.rezgas.com/results.php?area=ISL_south",
    "https://www.rezgas.com/results.php?area=mb_centre",
    "https://www.rezgas.com/results.php?area=mb_east",
    "https://www.rezgas.com/results.php?area=mb_interlakes",
    "https://www.rezgas.com/results.php?area=mb_north",
    "https://www.rezgas.com/results.php?area=mb_park",
    "https://www.rezgas.com/results.php?area=mb_pembina",
    "https://www.rezgas.com/results.php?area=mb_west",
    "https://www.rezgas.com/results.php?area=mb_winn",
    "https://www.rezgas.com/results.php?area=nb_acadia",
    "https://www.rezgas.com/results.php?area=nb_river",
    "https://www.rezgas.com/results.php?area=nl",
    "https://www.rezgas.com/results.php?area=ns",
    "https://www.rezgas.com/results.php?area=nwt",
    "https://www.rezgas.com/results.php?area=algoma",
    "https://www.rezgas.com/results.php?area=festival",
    "https://www.rezgas.com/results.php?area=getaway",
    "https://www.rezgas.com/results.php?area=JamesBay",
    "https://www.rezgas.com/results.php?area=lakeland",
    "https://www.rezgas.com/results.php?area=NearNorth",
    "https://www.rezgas.com/results.php?area=NSuperior",
    "https://www.rezgas.com/results.php?area=ontE",
    "https://www.rezgas.com/results.php?area=rainbow",
    "https://www.rezgas.com/results.php?area=sunset",
    "https://www.rezgas.com/results.php?area=southwest",
    "https://www.rezgas.com/results.php?area=baiejames",
    "https://www.rezgas.com/results.php?area=abitibi",
    "https://www.rezgas.com/results.php?area=OLLMontrealL",
    "https://www.rezgas.com/results.php?area=mauricie",
    "https://www.rezgas.com/results.php?area=saguenay",
    "https://www.rezgas.com/results.php?area=charlevoix",
    "https://www.rezgas.com/results.php?area=manicouagan",
    "https://www.rezgas.com/results.php?area=duplessisN",
    "https://www.rezgas.com/results.php?area=duplessisW",
    "https://www.rezgas.com/results.php?area=duplessisM",
    "https://www.rezgas.com/results.php?area=duplessisE",
    "https://www.rezgas.com/results.php?area=gaspesie"
]

provinces = {
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Newfoundland and Labrador": "NL",
    "Northwest Territories": "NT",
    "Nova Scotia": "NS",
    "Nunavut": "NU",
    "Ontario": "ON",
    "Prince Edward Island": "PE",
    "Quebec": "QC",
    "Saskatchewan": "SK",
    "Yukon": "YT"
}

def collect():
    data = pd.DataFrame(columns=["Name", "Address", "City", "Province", "Phone", "Extra"])
    for url in area_urls:
        eq_idx = url.find('=')
        print('\033[37m' + f"Collecting data from area: {url[eq_idx+1:]}")
        data = pd.concat([data, get_stations_info(url)])
    return data

def get_stations_info(url):
    driver.get(url)
    sidebar = driver.find_element(By.ID, "sidebar1")
    infos = []
    for item in sidebar.find_elements(By.TAG_NAME, "div"):
        ActionChains(driver).move_to_element(item).perform()
        info = item.find_element(By.TAG_NAME, "blockquote")
        lines = info.text.splitlines()
        row = []
        # Format data
        row.append(string.capwords(lines[0], sep=" "))
        # Address
        address = re.split(r"\ +", lines[1])
        for i, word in enumerate(address):
            if len(word) > 2:
                address[i] = string.capwords(word, sep=" ")
        row.append(" ".join(address))
        # City, province
        city = re.split(r",+", lines[2])
        if len(city) < 2:
            row.append("")
            if len(city[0]) > 2:
                    city[0] = string.capwords(city[0], sep=" ")
            row.append(city[0])
        else:
            city = re.split(r",\ +", lines[2])
            for i, word in enumerate(city):
                if len(word) > 2:
                    city[i] = string.capwords(word, sep=" ")
        row.append(city[0])
        if provinces.get(city[1]) is None:
            city[1] = city[1].upper()
        else:
            city[1] = provinces.get(city[1])
        row.append(city[1])
        # Phone
        row.append(lines[3])
        # Extra
        row.append(lines[4])
        
        print('\033[92m' + f"Found station info: {row}")
        infos.append(row)
    return pd.DataFrame(infos, columns=["Name", "Address", "City", "Province", "Phone", "Extra"])


if __name__ == "__main__":
    stations = collect()
    print('\033[37m' + f"Exporting to csv...")
    stations.to_csv("RezGasStations.csv", index=False)
    print('\033[92m' + f"Successfully exported to csv!")