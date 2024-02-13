import requests
from bs4 import BeautifulSoup
import openpyxl

def scrape(IDs):
    ans = []
    for id in IDs:
        link = 'https://www.guidestar.org/profile/' + id
        r = requests.get(link) 
        soup = BeautifulSoup(r.content, 'html.parser') 

        if soup.find('p', id="mission-statement") == None:
            continue
        print(link)
        mission = soup.find('p', id="mission-statement").text
        # location = soup.find('div', class_='description pt-3').find()
        name = soup.find('h1', class_='profile-org-name').text.strip()
        url = r.url
        new_row = (name, url, mission)
        ans.append(new_row)
        print('scraped: ' + id)
    return ans
    
def addToExcel(rows):
    workbook = openpyxl.load_workbook('data.xlsx')
    ws = workbook.active
    print('got to excel method')
    for row in rows:
        ws.append(row)
    workbook.save('data.xlsx')

def populateIDs():
    doc = open('EINs.txt', 'a')

    for i in range(1000000000):
        ein = format(i, '09d')
        ein = ein[0:2] + '-' + ein[2:]
        doc.write(ein + '\n')
        print('populated: ' + str(i))
    doc.close()

def main():
    r = requests.get("https://www.charitynavigator.org/ein/130552040") 
    soup = BeautifulSoup(r.content, 'html.parser') 
    mission = "Mission not available"
    if soup.find('span', class_="not-truncate") != None:
        mission = soup.find('span', class_="not-truncate").text
    print(mission)
    # location = soup.find('div', class_='description pt-3').find()
    # name = soup.find('h1', class_='profile-org-name').text.strip()
    # url = r.url
    # new_row = (name, url, mission)
    # print(new_row)

if __name__=="__main__":
    main()

