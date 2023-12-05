# Importing the required modules 
import os
import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim
import simplekml

def get_locator():
	return Nominatim(user_agent="mozilla")

def get_page(url):
	return requests.get(url).content

def exract_schools(html_data):
    data = []
    list_header = []
    soup = BeautifulSoup(html_data, "html.parser")
    table = soup.find_all("table")[0].find_all("tr")

    for items in table[0]:
        try:
            list_header.append(items.get_text().strip())
        except:
            continue

    for element in table[1:]:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text().strip())
            except:
                continue
        data.append(sub_data)

    return (list_header, data)

def save_csv(header, data):
    dataFrame = pd.DataFrame(data = data, columns = header)
    dataFrame.to_csv('schools.csv')

def save_kml(data):
    kml = simplekml.Kml()

    for school in data[1:]:
        try:
            geolocator = get_locator()
            pnt = kml.newpoint(name=school[2])
            location = geolocator.geocode(school[2])
            if location is None:
                print(f"Failed to get coordinates of: {school[2]}")
                continue
            pnt.address = school[2]
            pnt.coords = [(location.longitude, location.latitude)]
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
            pnt.description = f"{school[2]}\nRanking: {school[3]}\nSES: {school[11]}"
        except:
            print(f"Failed to get coordinates of: {school[2]}")
    kml.save("schools.kml")

def main():
    URL = "https://bettereducation.com.au/school/Primary/nsw/nsw_top_primary_schools_by_city.aspx?city=Newcastle"

    page = get_page(URL)

    header, data = exract_schools(page)
    save_csv(header, data)

    save_kml(data)


if __name__ == "__main__":
   main()
    