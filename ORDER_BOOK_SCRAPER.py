!#/usr/bin/python
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests
import datetime
'''-------------------------------------------------------------------------------------------*
    To run ORDER_BOOK_SCRAPER.py, navigate into the directory containing it. Make sure that
    option_file.txt contains the stock tickers of each company you want to look at on their
    own lines with no spaces after the name, that it is in the same directory as
    ORDER_BOOK_SCRAPER.py, and that the mysql server on your computer is running. Set the 
    DB_PATH variable to lead to the directory containing option_file.txt. Type 
    'python ORDER_BOOK_SCRAPER.py' into the command line, then the program will access the 
    current order book of every stock in option_file.txt and add the bids and asks to the 
    bids and asks tables of the financial_data database.
*-------------------------------------------------------------------------------------------'''
DB_PATH='home/ec2-user/EECS599/'

#Helpful functions.
def list_to_float(items):
    for i in range(len(items)):
        items[i] = float(items[i])

def list_remove_comma(items):
    for i in range(len(items)):
        items[i] = items[i].replace(",","")

#Bid and Ask classes for interaction with SQL database.
Base = declarative_base()

class Bid(Base):
    __tablename__='bids'

    id = Column(Integer, primary_key=True)
    cur_time = Column(String(50))
    company = Column(String(50))
    price = Column(Float)
    size = Column(Float)

    def __repr__(self):
        return "<Bid(date='%s', company='%s', price='%s', size='%s')" % (
                    self.cur_time, self.company, self.price, self.size)

class Ask(Base):
    __tablename__='asks'
    
    id = Column(Integer, primary_key=True)
    cur_time = Column(String(50))
    company = Column(String(50))
    price = Column(Float)
    size = Column(Float)
    
    def __repr__(self):
        return "<Ask(date='%s', company='%s', price='%s', size='%s')" % (
                    self.cur_time, self.company, self.price, self.size)

#Create table/class as well as engine to access the MySQL database named 'financial_data'.
engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_data')
Base.metadata.create_all(engine)

#Get current time.
now = str(datetime.datetime.now())[:19]

#Get the stock tickers from option_file.txt and put them into company_lst.
file = open('options.txt','r')
company_lst = file.readlines()
file.close()

#Remove the new line character from the end of each string element in company_lst.
for i in range(len(company_lst)):
    company_lst[i] = company_lst[i][:len(company_lst[i])-1]

#Create session for interaction with database using the engine created earlier.
Session = sessionmaker(bind=engine)
session = Session()

#Begin for-loop through company_tickers to scrape order books.
for i in range(len(company_lst)):
    company_name = company_lst[i]

    #Set up the BeautifulSoup object needed to scrape data.
    url = "http://finance.yahoo.com/q/ecn?s="+company_name+"+Order+Book"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    #Create necessary lists.
    needed_data = []
    bid_prices = []
    bid_sizes = []
    ask_prices = []
    ask_sizes = []

    #Access the table data tags from the beautiful soup object, if the tag has a non-empty string, add it to the needed_data list.
    tds = soup.find_all('td')
    for tag in tds:
        if(tag.string != None):
            needed_data.append(tag.string)
    for i in range(len(needed_data)):
        needed_data[i] = str(needed_data[i])

    #From the needed_data list, put the appropriate items into the bid_prices and bid_sizes lists.
    index = 0
    while(needed_data[2+index] != 'Price'):
        if(index%2 == 0):
            bid_prices.append(needed_data[2+index])
        else:
            bid_sizes.append(needed_data[2+index])
        index += 1

    #Remove sorted data from needed_data list.
    needed_data = needed_data[index+2:]

    #From the needed_data list, put the appropriate items into the ask_prices and ask_sizes lists.
    index = 0
    while(needed_data[2+index] != 'Last Trade:'):
        if(index%2 == 0):
            ask_prices.append(needed_data[2+index])
        else:
            ask_sizes.append(needed_data[2+index])
        index += 1

    #Convert bid_prices/ask_prices elements into floats.
    list_to_float(bid_prices)
    list_to_float(ask_prices)

    #Remove commas from bid_sizes/ask_sizes elements.
    list_remove_comma(bid_sizes)
    list_remove_comma(ask_sizes)

    #Convert bid_sizes/ask_sizes elements into floats.
    list_to_float(bid_sizes)
    list_to_float(ask_sizes)

    #Print Results to check.
    '''print"_____________________________________________________________"
    print "Company: "
    print company_name
    print "Bid Prices/Sizes: "
    print bid_prices
    print bid_sizes
    print ""
    print "Ask Prices/Sizes: "
    print ask_prices
    print ask_sizes
    print ""
    print "Time: "
    print now'''

    #For every element in the bid prices list, create a Bid instance using the current time, the company name, the bid price and the corresponding bid size. Add it to the financial_data database using session.add().
    for i in range(len(bid_prices)):
        bid = Bid(cur_time=now, company=company_name, price=bid_prices[i], size=bid_sizes[i])
        session.add(bid)

    #For evert element in the ask prices list, create an Ask instance using the current time, the company name, the ask price and the corresponding ask size. Add it to the financial_data database using session.add()
    for i in range(len(ask_prices)):
        ask = Ask(cur_time=now, company=company_name, price=ask_prices[i], size=ask_sizes[i])
        session.add(ask)

    #Save all additions to financial_data using session.commit().
    session.commit()

    #Check if in the database.
    '''bids = session.query(Bid).filter_by(company = company_name)
    for item in bids:
        print item

    asks = session.query(Ask).filter_by(company = company_name)
    for item in asks:
        print item'''





