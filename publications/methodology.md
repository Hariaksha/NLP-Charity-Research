**Data Collection**

The research dataset consists of many tax-exempt organizations in the United States. The most important data for each organization are the mission statements and the revenue. We obtain the EINs, addresses, NTEE codes, and financial information from the [Internal Revenue Service (IRS)](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf), which has information about all tax-exempt organizations in the United States organized in CSV files. The mission statements, organization names, and URLs were scraped from [GuideStar](https://www.guidestar.org/) and [Charity Navigator](https://www.charitynavigator.org/). The web scraper used to collect these data is titled 'guidestar_scraper.py' and is found in the 'scrapers' folder. This script uses the csv, requests, BeautifulSoup, time, and openpyxl Python libraries.

Each mission statement was preprocessed and tokenized using spaCy's 'en_core_web_lg' English NLP model.  

**Preliminary Data Analysis**

Before running our main analysis of labeling mission statement as more donor-serving or society-serving, we use the Quantitative Analysis of Textual Data R package (quanteda) to measure the linguistic richness and readability of each mission statement. We then find the relationship between each of these values and the revenue of each charity.

**Division of Data**

Before we begin our main analysis of the data, we organize our data by sectors and by assets. This allows us to see if overall linguistic trends and revenue relationships differ among sectors and among nonprofits with varying amounts of assets. The labeled NTEE codes and asset codes are pictured below.

| NTEE Code |  Sector                                                 | 
|:----------|:--------:                                               |
| A         | Arts, Culture, and Humanities                           | 
| B         |  Education                                              |
| C         | Environment                                             | 
| D         | Animal-Related                                          | 
| E         |  Healthcare                                             |
| F         | Mental Health & Crisis Intervention                     | 
| G         | Voluntary Health Associations & Medical Disciplines     | 
| H         |  Medical Research                                       |
| I         | Crime & Legal-Related                                   | 
| J         | Employment                                              | 
| K         |  Food, Agriculture and Nutrition                        |
| L         | Housing & Shelter                                       | 
| M         | Public Safety, Disaster Preparedness and Relief         |  
| N         |  Recreation & Sports                                    |
| O         | Youth Development                                       | 
| P         | Human Services                                          | 
| Q         |  International, Foreign Affairs and National Security   |
| R         | Civil Rights, Social Action & Advocacy                  | 
| S         | Community Improvement & Capacity Building               | 
| T         |  Philanthropy, Voluntarism and Grantmaking Foundations  |
| U         | Science & Technology                                    | 
| V         | Social Science                                          | 
| W         |  Public & Societal Benefit                              |
| X         | Religion-Related                                        |  
| Y         | Mutual & Membership Benefit                             | 
| Z         |  Unknown                                                |


| Asset Code |  Description ($)          | 
|:-----------|:-----------------:        |
| 0          | 0                         | 
| 1          |  1 to 9,999               |
| 2          | 10,000 to 24,999          | 
| 3          | 25,000 to 99,999          | 
| 4          |  100,000 to 499,999       |
| 5          | 500,000 to 999,999        | 
| 6          | 1,000,000 to 4,999,999    | 
| 7          | 5,000,000  to  9,999,999  |
| 8          |10,000,000  to  49,999,999 | 
| 9          | 50,000,000 to greater      | 



**Relating Mission Statement Language to Revenue**

We use NLP and statistics to determine the relationship between mission statement language and revenue. We see what linguistic structures and keywords influence fundraising efforts. 