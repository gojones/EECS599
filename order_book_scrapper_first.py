from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime



""" This program will ask the user for a company ticker for which they wish to scrape order book data from and the program will sort the order book into 4 lists: bid_prices, bid_sizes, ask_prices, and ask_sizes.
    Then, it connects to option_pricing_data.db, and adds the current time, company name,
    the bid prices/sizes, and ask prices/sizes to the order_book table contained within the
    database.
    Finally, it will present the user with the option of whether or not to commit the additions
    to the database. """
### Need to edit so that it continually loops adding a lot of data to the database. ###
### Afterward need to figure out how to get it running on an ec2 machine through amazon. ###

#User-defined functions.
def list_convert_to_float(items):
    for i in range(len(items)):
        items[i] = float(items[i])

def list_remove_comma(items):
    for i in range(len(items)):
        items[i] = items[i].replace(",","")


#Set up the BeautifulSoup object needed to scrape data.
company_name = raw_input("Enter company's ticker you would like order book data from: ")
company_name = company_name.upper()
url = "http://finance.yahoo.com/q/ecn?s="+company_name+"+Order+Book"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

#Get current time.
now = str(datetime.datetime.now())[:19]

#Create lists used for storing scraped data
needed_data = []
bid_prices = []
bid_sizes = []
ask_prices = []
ask_sizes = []

#Aquire the needed table data from the yahoo finance page, store into the list tds
tds = soup.find_all('td')

#Put the tds elemetns into the needed_data list, where it will be put into the
#appropriate lists
for tag in tds:
    if(tag.string != None):
        needed_data.append(tag.string)

#Convert needed_data elements into normal strings instead of unicode strings.
#(not sure if necessary?)
for i in range(len(needed_data)):
    needed_data[i] = str(needed_data[i])

#Create index for while loop.
index = 0

#Populate the bid_prices and bid_sizes lists.
while(needed_data[2+index] != 'Price'):
    if(index%2 == 0):
        bid_prices.append(needed_data[2+index])
    else:
        bid_sizes.append(needed_data[2+index])
    index = index + 1

#Remove sorted data from needed_data list.
needed_data = needed_data[index+2:]

#Populate the ask_prices and ask_sizes lists.
index = 0
while(needed_data[2+index] != 'Last Trade:'):
    if(index%2 == 0):
        ask_prices.append(needed_data[2+index])
    else:
        ask_sizes.append(needed_data[2+index])
    index = index+1

#Convert bid_prices/ask_prices elements into floats.
list_convert_to_float(bid_prices)
list_convert_to_float(ask_prices)

#Remove commas from bid_sizes/ask_sizes elements so that they can be converted into floats.
list_remove_comma(bid_sizes)
list_remove_comma(ask_sizes)

#Convert bid_sizes/ask_sizes elements into floats.
list_convert_to_float(bid_sizes)
list_convert_to_float(ask_sizes)

#Print Results to check.
print"_____________________________________________________________"
print "Bid Prices/Sizes: "
print bid_prices
print bid_sizes
print ""
print "Ask Prices/Sizes: "
print ask_prices
print ask_sizes
print ""
print "Time: "
print now

#Have user input whether or not the table has been created.
'''table_flag = raw_input("Has the order book table already been created? Enter 1 for yes, 0 for no: ")
table_flag = int(table_flag)'''

#Create the connection to database and the cursor object.
conn = sqlite3.connect('option_pricing_data.db')
c = conn.cursor()

'''#Create table if it hasn't been created already.
if (table_flag == 0):
    c.execute(CREATE TABLE order_book
                    (date text, company text, bid text, price_b real, size_b real, ask text, price_a real, size_a real))'''

#Insert values into database table.
#For when there are the same amount of bids and asks.
if(len(bid_prices) == len(ask_prices)):
    for i in range(len(ask_prices)):
        temp = (now, company_name, 'BID', bid_prices[i], bid_sizes[i], 'ASK', ask_prices[i], ask_sizes[i])
        c.execute('INSERT INTO order_book VALUES (?,?,?,?,?,?,?,?)', temp)

#For when there are more asks than bids
if(len(bid_prices) < len(ask_prices)):
    counter = 0
    for i in range(len(bid_prices)):
        temp = (now, company_name, 'BID', bid_prices[i], bid_sizes[i], 'ASK', ask_prices[i], ask_sizes[i])
        c.execute('INSERT INTO order_book VALUES (?,?,?,?,?,?,?,?)', temp)
        counter = counter+1
    while (counter < len(ask_prices)):
        temp = (now, company_name, 'BID', 0, 0, 'ASK', ask_prices[counter], ask_sizes[counter])
        c.execute('INSERT INTO order_book VALUES (?,?,?,?,?,?,?,?)', temp)
        counter = counter + 1

#For when there are more bids than asks
if(len(ask_prices) < len(bid_prices)):
    counter = 0
    for i in range(len(ask_prices)):
        temp = (now, company_name, 'BID', bid_prices[i], bid_sizes[i], 'ASK', ask_prices[i], ask_sizes[i])
        c.execute('INSERT INTO order_book VALUES (?,?,?,?,?,?,?,?)', temp)
        counter = counter+1
    while (counter < len(bid_prices)):
        temp = (now, company_name, 'BID', bid_prices[counter], bid_sizes[counter], 'ASK', 0, 0)
        c.execute('INSERT INTO order_book VALUES (?,?,?,?,?,?,?,?)', temp)
        counter = counter + 1




#Save changes to the database.
com_change = raw_input("Commit changes to the database? Enter 1 for yes, 0 for no: ")
com_change = int(com_change)

if(com_change == 1):
    conn.commit()

#Close connection to database.
conn.close()




