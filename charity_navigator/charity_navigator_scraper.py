import requests
from bs4 import BeautifulSoup
import csv
import openpyxl
import time

def scrape():
    ans = []
    doc = open('EINs.txt')

    while True:
        line = doc.readline()
        if not line:
            break
        
        r = requests.get(line) 
        soup = BeautifulSoup(r.content, 'html.parser') 

        if soup.find('p', id="mission-statement") == None:
            continue
        mission = soup.find('p', id="mission-statement").text
        # location = soup.find('div', class_='description pt-3').find()
        name = soup.find('h1', class_='profile-org-name').text.strip()
        url = r.url
        new_row = (name, url, mission)
        ans.append(new_row)
        print('scraped: ' + id)
    doc.close()
    return ans
    
def addToExcel(rows):
    workbook = openpyxl.load_workbook('data.xlsx')
    ws = workbook.active
    print('got to excel method')
    for row in rows:
        ws.append(row)
    workbook.save('data.xlsx')

def numToEIN(num):
    return format(num, '09d')

def all():
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
        
def main():
    all()
    
if __name__=="__main__":
    main()

