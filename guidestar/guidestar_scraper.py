import requests
from bs4 import BeautifulSoup
import openpyxl
import csv
import time

def numToEIN(num):
    ans = format(num, '09d')
    ans = ans[0:2] + '-' + ans[2:]
    return ans

def main():
    filename = open('exempt_organizations_excel\eo_nd.csv') # CHANGE
    file = csv.DictReader(filename)
    workbook = openpyxl.load_workbook('guidestar/data/ND_data.xlsx') # CHANGE
    ws = workbook.active
    ws2 = workbook.create_sheet("Skipped")
    ws2.append(["Skipped EIN", "Name from IRS Spreadsheet", "Guidestar Link"])
    for col in file:
        time.sleep(0.85) # 0.7 is too fast
        ein = numToEIN(int(col['EIN']))
        link = f"https://www.guidestar.org/profile/{ein}"
        r = requests.get(link) 
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.title.text)
        if soup.title.text == "":
            new_row = (ein, col['NAME'], link)
            ws2.append(new_row)
            continue
        mission = soup.find('p', id="mission-statement").text
        if mission == "This organization has not provided GuideStar with a mission statement.":
            r2 = requests.get(f"https://www.charitynavigator.org/ein/{format(int(col['EIN']), '09d')}")
            soup2 = BeautifulSoup(r2.content, 'html.parser')
            if soup2.find('span', class_="not-truncate") != None:
                mission = soup2.find('span', class_="not-truncate").text
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
    workbook.save('guidestar/data/ND_data.xlsx') # CHANGE
    
if __name__=="__main__":
    main()
