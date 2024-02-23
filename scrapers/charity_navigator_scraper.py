import requests
from bs4 import BeautifulSoup
import csv
import openpyxl
import time

def numToEIN(num):
    return format(num, '09d')
        
def main():
    filename = open('exempt_organizations_excel\eo_al.csv')
    file = csv.DictReader(filename)
    skipped = 0
    for col in file:
        time.sleep(1)
        ein = numToEIN(int(col['EIN']))
        link = "https://www.charitynavigator.org/ein/" + ein
        name = col['NAME']
        street = col['STREET']
        city = col['CITY']
        state = col['STATE']
        zip = col['ZIP']

        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        print(link + ": " + soup.title.text)
        if soup.title.text == "Charity Navigator: 406 Forbidden":
            skipped += 1
            continue
        
        mission = "Mission not available"
        if soup.find('span', class_="not-truncate") != None:
            mission = soup.find('span', class_="not-truncate").text
        rating = "N/A"
        s = soup.find('div', id='overall-rating-section-2')
        if s.find('strong') != None:
            rating = s.find('strong').text

        new_row = (ein, name, street, city, state, zip, link, "", mission, rating)
        workbook = openpyxl.load_workbook('charity_navigator/Data.xlsx')
        ws = workbook.active
        ws.append(new_row)
        workbook.save('charity_navigator/Data.xlsx')
    print("Skipped: " + skipped)

if __name__=="__main__":
    main()

