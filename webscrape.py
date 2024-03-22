import requests
from bs4 import BeautifulSoup
import openpyxl
import csv
import time

def get_request(link):
    while True:  
        try:
            x = requests.get(link)
            ans = BeautifulSoup(x.content, 'html.parser')
            break
        except:
            print('Connection lost. Retrying in 10 seconds.')
            time.sleep(10)
    return ans

def numToEIN(num):
    ans = format(num, '09d')
    ans = ans[0:2] + '-' + ans[2:]
    return ans

def main():
    state = 'TN' # CHANGE
    filename = open(f'data/american/irs-exempt-orgs/eo_{state.lower()}.csv') 
    file = csv.DictReader(filename)
    workbook = openpyxl.load_workbook(f'data/{state.upper()}_data.xlsx')
    ws = workbook.active
    ws2 = workbook['Skipped']
    print("Press 'Ctrl-C' to exit the loop")
    try:
        for col in file:
            time.sleep(1) 
            ein = numToEIN(int(col['EIN']))
            link = f"https://www.guidestar.org/profile/{ein}"
            soup = get_request(link)
            errors = {
                "www.guidestar.org | 502: Bad gateway": "fixing 502 bad gateway error",
                "502 Bad Gateway": "fixing 502 bad gateway error",
                "www.guidestar.org | 504: Gateway time-out": "fixing 504 gateway time-out error",
                "504: Gateway time-out": "fixing 504 gateway time-out error",
                "www.guidestar.org | 520: Web server is returning an unknown error": "web server encountered unknown error.",
                "Access denied | www.guidestar.org used Cloudflare to restrict access": "Access denied"
            }
            while soup.title.text in errors:
                print(errors[soup.title.text])
                print("Retrying in 10 seconds.")
                time.sleep(10)
                soup = get_request(link)
            print(ein, soup.title.text)
            if soup.title.text == "": 
                # if GuideStar does not have a page for this org, add it to the skipped list
                ws2.append([ein, col['NAME'], link])
                print(f"Skipped: {ein} {soup.title.text}")
                continue
            mission = soup.find('p', id="mission-statement").text 
            if mission == "This organization has not provided GuideStar with a mission statement.":
                soup2 = get_request(f"https://www.charitynavigator.org/ein/{format(int(col['EIN']), '09d')}")
                mission = mission if soup2.find('span', class_="not-truncate") == None else soup2.find('span', class_="not-truncate").text
            mission = '' if mission == 'This organization has not provided GuideStar with a mission statement.' else mission
            name = soup.find('h1', class_='profile-org-name').text.strip()
            url = '' if soup.find('a', class_='hide-print-url') == None else soup.find('a', class_='hide-print-url').text
            ws.append([ein, name, col['STREET'], col['CITY'], state, col['ZIP'], link, url, col['NTEE_CD'], col['DEDUCTIBILITY'], col['ASSET_CD'], col['ASSET_AMT'], col['INCOME_CD'], col['INCOME_AMT'], col['REVENUE_AMT'], mission])
    except KeyboardInterrupt:
        pass
    workbook.save(f'data/{state.upper()}_data.xlsx') 
    print("Saved")

if __name__=="__main__":
    main()