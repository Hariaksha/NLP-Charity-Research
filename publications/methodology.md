**Data Collection**

The research dataset consists of many tax-exempt organizations in the United States. The most important data for each organization are the mission statements and the revenue. We obtain the EINs, addresses, NTEE codes, and financial information from the [Internal Revenue Service (IRS)](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf), which has information about all tax-exempt organizations in the United States organized in CSV files. The mission statements, organization names, and URLs were scraped from [GuideStar](https://www.guidestar.org/) and [Charity Navigator](https://www.charitynavigator.org/). The web scraper used to collect these data is titled 'guidestar_scraper.py' and is found in the 'scrapers' folder. This script uses the csv, requests, BeautifulSoup, time, and openpyxl Python libraries.

Each mission statement was preprocessed and tokenized using spaCy's 'en_core_web_lg' English NLP model.  

**Comparing Sectors**

First, to compare industries or sectors, we separated organizations by their NTEE code.

**Relating Mission Statement Language to Revenue**

We use NLP and statistics to determine the relationship between mission statement language and revenue. We see what linguistic structures and keywords influence fundraising efforts. 