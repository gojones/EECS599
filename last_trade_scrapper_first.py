from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

""" This program will ask the user for a company ticker for which they wish to scrape last trade data from. 
    The program will then connect to option_pricing_data.db and adds the current time, company
    name, last trade value, and last trade time to the last_trade table contained within the
    database.
    Finally, it will present the user with the option of whether or not to comit the additions 
    to the database. """
### Need to edit so that it continually loops adding a lot of data to the database. ###
### Afterward need to figure out how to get it running on an ec2 machine through amazon. ###

#Set up the BeautifulSoup object needed to scrape data.
company_name = raw_input("Enter the company's ticker you would like last trade data from: ")
company_name = company_name.upper()
url = "http://finance.yahoo.com/q/ecn?s="+company_name+"+Order+Book"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

#Get current date/time.
now = str(datetime.datetime.now())
now = now[:19]

#Create lists used for storing scraped data.
needed_data = []

#Populate the needed_data list.
for tag in soup.find_all('td'):
    if(tag.string != None):
        needed_data.append(tag.string)

#Convert needed_data contents to normal strings instead of unicode strings.
for i in range(len(needed_data)):
    needed_data[i] = str(needed_data[i])

#Create index for while loop.
index = 0

#Find last trade index.
while(needed_data[index] != 'Last Trade:'):
    index += 1

#Put last trade value and last trade time into their own variables.
last_trade_val = float(needed_data[index+1])
last_trade_time = needed_data[index+3]

#Print Results to check.
print"_____________________________________________________________"
print "Last Trade: "+str(last_trade_val)
print "Time: "+last_trade_time

#Create the connection to database and the cursor object.
conn = sqlite3.connect('option_pricing_data.db')
c = conn.cursor()

#Insert values into database table.
temp = (now, company_name, 'Last Trade: ', last_trade_val, 'Time: ', last_trade_time)
c.execute('INSERT INTO last_trade VALUES (?,?,?,?,?,?)', temp)

#Save changes to the database.
com_change = raw_input("Commit changes to the database? Enter 1 for yes, 0 for no: ")
com_change = int(com_change)
if(com_change == 1):
    conn.commit()

#Close connection to database.
conn.close()





