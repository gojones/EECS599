from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

""" This program will as the user for a company ticker, and will the scrape option data from that companies yahoo finance page. 
    It will then connect to option_pricing_data.db and add the current time, 
    company name, call/put option, strike price, bid price, ask price, and
    expiration date to the options table. 
    Finally it will present the user with the option of whether or not to commit
    the additions to the database. """
### Need to edit so that it continually loops adding a lot of data to the database. ###
### Afterward need to figure out how to get it running on an ec2 machine through amazon. ###

#Get company_lst from options.txt
file = open('options.txt','r')
company_lst = file.readlines()
file.close()
for i in range(len(company_lst)):
    company_lst[i] = company_lst[i][:len(company_lst[i])-1]

#Begin for-loop for scrapping options data.
for i in range(len(company_lst)):
    company_name = company_lst[i]

    #Set up the BeautifulSoup object needed to scrape data.
    url = "http://finance.yahoo.com/q/op?s="+company_name+"+Options"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    #Get current time.
    now = str(datetime.datetime.now())[:19]

    #Create lists for storing scrapped data.
    needed_data = []

    #Populate the needed_data list.
    for tag in soup.find_all('td'):
        if (tag.string != None):
            needed_data.append(tag.string)

    #Get expiration_date for call options.
    slice = 0
    if(len(needed_data) > 2):
        date_block = needed_data[2]
        while(date_block[slice] != ','):
            slice += 1

        expiration_date = date_block[slice+2:]


        #Print current time and expiration_date list for checking purposes.
        #print "_____________________________________________________________"


        #edit needed_data list for data extraction.
        needed_data = needed_data[3:]

        #set index for while loop.
        index = 0

        #Connect to option_pricing_data.db
        conn = sqlite3.connect('option_pricing_data.db')
        c = conn.cursor()

        #Loop to add Call Options to the database.
        while(needed_data[index] != 'Put Options'):
            strike1 = needed_data[index]
            bid1 = needed_data[index+3]
            ask1 = needed_data[index+4]
            temp = (now, company_name, "CALL", "strike: ", float(strike1), "bid: ", str(bid1), "ask: ", str(ask1), str(expiration_date))
            c.execute('INSERT INTO options VALUES (?,?,?,?,?,?,?,?,?,?)', temp)
            #print temp
            index +=7

        index += 2

        #Loop to add Put Options to the database.
        while(index < (len(needed_data)-10)):
            pstrike1 = needed_data[index]
            pbid1 = needed_data[index+3]
            pask1 = needed_data[index+4]
            temp2 = (now, company_name, "PUT", "strike: ", float(pstrike1), "bid: ", str(pbid1), "ask: ", str(pask1), str(expiration_date))
            c.execute('INSERT INTO options VALUES (?,?,?,?,?,?,?,?,?,?)', temp2)
            #print temp2
            index += 7

        #Save changes to the database.
        conn.commit()

        #Close connection to database.
        conn.close()









