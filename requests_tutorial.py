import requests # library to make HTTP requests to a specific URL and returns the response
# https://www.geeksforgeeks.org/python-web-scraping-tutorial/

# We must understand structure of page before getting desired info from the HTML. Use Inspect Element

# Make a request
r = requests.get("https://www.guidestar.org/")

# Print status code for response received
# success code - 200
print(r)
print(r.status_code)

# Print request object
print(r.url)

# Print content of request
print(r.content)