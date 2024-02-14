import requests
from bs4 import BeautifulSoup
import openpyxl
import csv
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

def populateAllIDs():
    doc = open('guidestar.txt', 'a')

    for i in range(18796978, 1000000000):
        ein = format(i, '09d')
        ein = ein[0:2] + '-' + ein[2:]
        ein = 'https://www.guidestar.org/profile/' + ein
        doc.write(ein + '\n')
        print('populated: ' + str(i))
    doc.close()

def numToEIN(num):
    ans = format(num, '09d')
    ans = ans[0:2] + '-' + ans[2:]
    return ans

def populateGoodIDs():
    doc = open('guidestar_good_links.txt', 'a')

    for i in range(100): #1000000000
        ein = numToEIN(i)   
        link = 'https://www.guidestar.org/profile/' + ein
        r = requests.get(link) 
        soup = BeautifulSoup(r.content, 'html.parser')
        if soup.find('p', id="mission-statement") != None:
            doc.write(link + '\n')
            print('populated: ' + str(i))
    doc.close()

def all():
    filename = open('exempt_organizations_excel\eo_wy.csv') # CHANGE
    file = csv.DictReader(filename)
    workbook = openpyxl.load_workbook('guidestar/data/WY_data.xlsx') # CHANGE
    ws = workbook.active
    skipped = []
    for col in file:
        time.sleep(0.7) # 0.6 is too fast
        ein = numToEIN(int(col['EIN']))
        link = f"https://www.guidestar.org/profile/{ein}"
        r = requests.get(link) 
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.title.text)
        if soup.title.text == "":
            skipped.append(ein)
            continue
        mission = soup.find('p', id="mission-statement").text
        if mission == "This organization has not provided GuideStar with a mission statement.":
            r2 = requests.get(f"https://www.charitynavigator.org/ein/{format(int(col['EIN']), '09d')}")
            soup2 = BeautifulSoup(r2.content, 'html.parser')
            if soup.find('span', class_="not-truncate") != None:
                mission = soup.find('span', class_="not-truncate").text
        name = soup.find('h1', class_='profile-org-name').text.strip()
        url = ""
        if soup.find('a', class_='hide-print-url') != None:
            url = soup.find('a', class_='hide-print-url').text
        street = col['STREET']
        city = col['CITY']
        state = col['STATE']
        zip = col['ZIP']
        ntee = col['NTEE_CD']
        new_row = (ein, name, street, city, state, zip, link, url, ntee, mission)
        ws.append(new_row)
    ws.append((f"Skipped: {len(skipped)}"))
    for id in skipped:
        ws.append((id))
    workbook.save('guidestar/data/WY_data.xlsx') # CHANGE
        
def main():
    all()
    
if __name__=="__main__":
    main()

