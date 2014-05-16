from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
import requests
import datetime
'''-------------------------------------------------------------------------------------------*
    To run OPTION_SCRAPER.py, navigate into the directory containing it. Make sure that
    option_file.txt contains the stock tickers of each company you want to look at on their
    own lines with no spaces after the name, that it is in the same directory as
    OPTION_SCRAPER.py, and that the mysql server on your computer is running. Set the DB_PATH
    variable to lead to the directory containing option_file.txt. Type 'python OPTION_SCRAPER.py'
    into the command line, then the program will access and add the current call and put 
    options of every stock in option_file.txt to the options table of the financial_data database.
*-------------------------------------------------------------------------------------------'''
DB_PATH = '/Users/gojones26/Desktop/Classes/EECS599/'

#Option class for interaction with SQL database.
Base = declarative_base()

class Option(Base):
    __tablename__ = 'options'

    id = Column(Integer, primary_key=True)
    cur_time = Column(String(50))
    company = Column(String(50))
    type = Column(String(50))
    strike_price = Column(Float)
    last_trade = Column(String(50))
    bid_price = Column(String(10))
    ask_price = Column(String(10))
    exp = Column(String(50))

    def __repr__(self):
        return "<Option(date='%s', company='%s', type='%s', strike='%s', last='%s', bid='%s', ask='%s', expires='%s')>" % (
                    self.cur_time, self.company, self.type, self.strike_price, self.last_trade, self.bid_price, self.ask_price, self.exp)

#Create table/class as well as engine to access the MySQL database named 'financial_data'.
engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_data')
Base.metadata.create_all(engine)

#Get current time.
now = str(datetime.datetime.now())[:19]

#Get the stock tickers from option_file.txt and put them into company_lst.
file = open(DB_PATH+'option_file.txt', 'r')
company_lst = file.readlines()
file.close()

#Remove the new line character from the end of each string element in company_lst.
for i in range(len(company_lst)):
    company_lst[i] = company_lst[i][:len(company_lst[i])-1]

#Create session for interaction with database using the engine created earlier.
Session = sessionmaker(bind=engine)
session = Session()

#Begin for-loop through company tickers to scrape options.
for i in range(len(company_lst)):
    company_name = company_lst[i]

    #Set up the BeautifulSoup object needed to scrape data.
    url = "http://finance.yahoo.com/q/op?s="+company_name+"+Options"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    #Create needed_data list, access the table data tags from the beautiful soup object, if the tag has a non-empty string, add it to the needed_data list.
    needed_data = []
    for tag in soup.find_all('td'):
        if(tag.string != None):
            needed_data.append(tag.string)

    #Get expiration_date from the needed_data list.
    slice = 0
    if(len(needed_data) > 2):
        date_block = needed_data[2]
        while(date_block[slice] != ','):
            slice += 1

        expiration_date = date_block[slice+2:]

        #Remove unnecessary elements from needed data list.
        needed_data = needed_data[3:]

        #set index for while loop.
        index = 0

        #Loop through the call options in the needed_data list, extract strike, bid, ask for each one, create Option instance using these, the current time, the company name, and the string 'CALL', then add the Option instance to the financial_data database using session.add().
        while(needed_data[index] != 'Put Options'):
            cstrike = needed_data[index]
            clast = needed_data[index+2]
            cbid = needed_data[index+3]
            cask = needed_data[index+4]
            temp = Option(cur_time=now, company=company_name, type='CALL', strike_price=float(cstrike), last_trade=str(clast), bid_price=str(cbid), ask_price=str(cask), exp=str(expiration_date))
            session.add(temp)
            print temp
            index += 7

        #Save addition of the call options using session.commit().
        #session.commit()

        #Increment index in order to access the put option data.
        index += 2

        #Loop through the put options in the needed_data list, extract strike, bid, ask for each one, create Option instance using these, the current time, the company name, and the string 'PUT', then add the Option instance to the financial_data database using session.add().
        while(index < (len(needed_data)-10)):
            pstrike = needed_data[index]
            plast = needed_data[index+2]
            pbid = needed_data[index+3]
            pask = needed_data[index+4]
            temp2 = Option(cur_time=now, company=company_name, type='PUT', strike_price=float(pstrike), last_trade=str(plast), bid_price=str(pbid), ask_price=str(pask), exp=str(expiration_date))
            session.add(temp2)
            index += 7

        #Save addition of the put options using session.commit().
        session.commit()
