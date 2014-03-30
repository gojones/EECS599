from bs4 import BeautifulSoup
import requests

#Get company ticker from user
company_name = raw_input("Enter the company ticker you want the current stock price for: ")
company_name = company_name.upper()

#Set up the BeautifulSoup object needed to scrape data.
url = "http://finance.yahoo.com/q/ecn?s="+company_name+"+Order+Book"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

#Create and populate list of scraped data in order to access the current stock price.
needed_data = []
for tag in soup.find_all('span'):
    if (tag.string != None):
        needed_data.append(tag.string)

#Retrieve current stock price from needed_data list.
current_price = needed_data[14]

print "Current Stock price for "+company_name+": "+current_price

