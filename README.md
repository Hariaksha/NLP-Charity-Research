I started this project in January 2024 with Dr. Michael Price, a Professor of Economics at The University of Alabama with research projects related to charitable giving.

The project involves gathering mission statements from tax-exempt organizations (nonprofits/charities) from the United States, the United Kingdom, Australia, and Canada. We used the Python requests and BeautifulSoup libraries to accomplish this with web scraping. The United States data was scraped from GuideStar and Charity Navigator. The main scraper that we used is titled 'guidestar_scraper.py' and is found in the 'scrapers' folder. 

Afterwards, we used Natural Language Processing techniques to identify patterns among these mission statements, with the goal of seeing how mission statements impact fundraising. We hope that this research benefits future charitable giving.

The 'tutorials' folder contains files that I used to learn how to use various libraries, particularly the libraries involving Natural Language Processing tasks. 

The 'scrapers' folder contains Python web scraping scripts, but this project only used the one titled guidestar_scraper.py.

The 'exempt_organizations' folder contains information in CSV files from the United States Internal Revenue Service about tax-exempt organizations. This data was very useful in finding mission statements because they provide the EINs for every tax-exempt organization in the United States, separated by states and D.C.

The data (mission statements, EINs, nonprofits' names, etc.) are found in the 'data' folder. The United States data are organized by states and D.C. and labeled as (state abbreviation)_data.xlsx (example: AL_data.xlsx). There is also a master spreadsheet that combines the information from all of the 51 other spreadsheets.