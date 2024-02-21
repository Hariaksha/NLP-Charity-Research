import requests
from bs4 import BeautifulSoup
import openpyxl
import csv
import time

def check_internet(url='https://www.google.com', timeout=5):
    # put the below three lines in the for loop in the main function to implement 
    # while check_internet() is False:
    #     print("Connection lost")
    #     time.sleep(1)
    try:
        # Try to request Google. If successful, internet is working.
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        # Internet is not working.
        return False 

def numToEIN(num):
    ans = format(num, '09d')
    ans = ans[0:2] + '-' + ans[2:]
    return ans

def main():
    # MUST CHANGE STATE ABBREVIATION FOUR TIMES IN THIS FUNCTION
    filename = open('exempt_organizations/eo_ak.csv') # CHANGE
    file = csv.DictReader(filename)
    workbook = openpyxl.load_workbook('guidestar/data/AK_data.xlsx') # CHANGE
    ws = workbook.active
    ws2 = workbook.create_sheet("Skipped")
    ws2.append(["Skipped EIN", "Name from IRS Spreadsheet", "Guidestar Link"])
    state = 'AK' # CHANGE
    for col in file:
        time.sleep(1) # 0.84 is too fast
        ein = numToEIN(int(col['EIN']))
        link = f"https://www.guidestar.org/profile/{ein}"
        r = requests.get(link) 
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.title.text)
        if soup.title.text == "": 
            # if GuideStar does not have a page for this org, add it to the skipped list
            new_row = (ein, col['NAME'], link)
            ws2.append(new_row)
            continue
        mission = soup.find('p', id="mission-statement").text 
        if mission == "This organization has not provided GuideStar with a mission statement.":
            r2 = requests.get(f"https://www.charitynavigator.org/ein/{format(int(col['EIN']), '09d')}")
            soup2 = BeautifulSoup(r2.content, 'html.parser')
            if soup2.find('span', class_="not-truncate") != None:
                mission = soup2.find('span', class_="not-truncate").text
        if mission == "This organization has not provided GuideStar with a mission statement.":
            mission = ''
        name = soup.find('h1', class_='profile-org-name').text.strip()
        url = ""
        if soup.find('a', class_='hide-print-url') != None:
            url = soup.find('a', class_='hide-print-url').text
        revenue = col['REVENUE_AMT']
        income_code = col['INCOME_CD']
        income = col['INCOME_AMT']
        street = col['STREET']
        city = col['CITY']
        asset_code = col['ASSET_CD']
        assets = col['ASSET_AMT']
        zip = col['ZIP']
        ntee = col['NTEE_CD']
        deductibility = col['DEDUCTIBILITY']
        new_row = (ein, name, street, city, state, zip, link, url, ntee, deductibility, asset_code, assets, income_code, income, revenue, mission)
        ws.append(new_row)
    workbook.save('guidestar/data/AK_data.xlsx') # CHANGE
    
if __name__=="__main__":
    main()
