import requests
from bs4 import BeautifulSoup
import openpyxl

def scrape(link):
    r = requests.get(link) 
    soup = BeautifulSoup(r.content, 'html.parser') 

    if soup.find('p', id="mission-statement") == None:
        return
    
    mission = soup.find('p', id="mission-statement").text
    # location = soup.find('div', class_='description pt-3').find()
    name = soup.find('h1', class_='profile-org-name').text.strip()
    url = r.url
    new_row = (name, url, mission)

    workbook = openpyxl.load_workbook('data.xlsx')
    ws = workbook.active
    ws.append(new_row)
    workbook.save('data.xlsx')

def iterateID():
    for i in range(100): #1000000000
        ein = format(i, '09d')
        ein = ein[0:2] + '-' + ein[2:]
        ein = "https://www.guidestar.org/profile/" + ein
        scrape(ein)

iterateID()