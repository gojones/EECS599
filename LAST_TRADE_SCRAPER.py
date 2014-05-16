from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
import requests
import datetime
'''-------------------------------------------------------------------------------------------*
    To run LAST_TRADE_SCRAPER.py, navigate into the directory containing it. Make sure that
    option_file.txt contains the stock tickers of each company you want to look at on their
    own lines with no spaces after the name, that it is in the same directory as
    OPTION_SCRAPER.py, and that the mysql server on your computer is running. Set the DB_PATH 
    variable to lead to the directory containing option_file.txt. Type 
    'python LAST_TRADE_SCRAPER.py' into the command line, then the program will access and
    add the last trade for every stock in option_file.txt to the last_trade table of the 
    financial_data database.
*-------------------------------------------------------------------------------------------'''
DB_PATH = '/home/ec2-user/EECS599/'

#LastTrade class for interaction with last_trade table.
Base = declarative_base()

class LastTrade(Base):
    __tablename__ = 'last_trade'

    id = Column(Integer, primary_key=True)
    cur_time = Column(String(50))
    company = Column(String(50))
    trade_val = Column(Float)
    trade_time = Column(String(50))

    def __repr__(self):
        return "<Last_Trade(date='%s', company='%s', trade_val='%s', trade_time = '%s')>" % (
                            self.cur_time, self.company, self.trade_val, self.trade_time)

#Create table/class as well as engine to access the MySQL database named 'financial_data'.
engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_data')
Base.metadata.create_all(engine)

#Get current time.
now = str(datetime.datetime.now())[:19]

#Get the stock tickers from option_file.txt and put them into company_lst.
file = open('option_file.txt', 'r')
company_lst = file.readlines()
file.close()

#Remove the new line character from the end of each string element in company_lst.
for i in range(len(company_lst)):
    company_lst[i] = company_lst[i][:len(company_lst[i])-1]

#Create session for interaction with database using the engine created earlier.
Session = sessionmaker(bind=engine)
session = Session()

#Begin for-loop through company tickers to scrape trades.
for i in range(len(company_lst)):
    company_name = company_lst[i]

    #Set up the BeautifulSoup object needed to scrape data.
    url = "http://finance.yahoo.com/q/ecn?s="+company_name+"+Order+Book"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    #Create needed_data list, access the table data tags from the beautiful soup object, if the tag has a non-empty string, add it to the needed_data list.
    needed_data = []
    for tag in soup.find_all('td'):
        if(tag.string != None):
            needed_data.append(tag.string)

    #Create index for while loop.
    index = 0

    #If the needed_data list contains less than 9 elements, the last trade value is currently unavailable.
    if(len(needed_data) > 9):
        #Find the last trade index in the needed data list.
        while(needed_data[index] != 'Last Trade:'):
            index += 1

        #Put last trade value and last trade time into their own variables.
        last_trade_val = float(needed_data[index+1])
        last_trade_time = needed_data[index+3]

        #Print the company, the company ticker, the last trade value, and the last trade time in order to check that the values are what they should be.
        '''print "Company: "
            print company_name
            print "Last Trade: "+str(last_trade_val)
            print "Time: "+last_trade_time'''

        #Create a LastTrade instance using the current time, company name, the last trade value and the last trade time, then add the LastTrade instance to the database using session.add() and save the addition using session.commit().
        trade = LastTrade(cur_time=now, company=company_name, trade_val=last_trade_val, trade_time=last_trade_time)
        session.add(trade)
        session.commit()


