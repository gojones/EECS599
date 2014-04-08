!#/usr/bin/python
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests
import datetime

"""Order book scraper using sqlalchemy to store in the database."""

#Helpful functions.
def list_to_float(items):
    for i in range(len(items)):
        items[i] = float(items[i])

def list_remove_comma(items):
    for i in range(len(items)):
        items[i] = items[i].replace(",","")

#Bid and ask classes for interaction with SQL database
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

#Create table/class if needed.
engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_data')
Base.metadata.create_all(engine)

#Get current time.
now = str(datetime.datetime.now())[:19]

#Get company_lst from options.txt (FIX LATER).
file = open('options.txt','r')
company_lst = file.readlines()
file.close()

for i in range(len(company_lst)):
    company_lst[i] = company_lst[i][:len(company_lst[i])-1]

#Begin for-loop for scraping last_trade data.
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

    #Get needed_table data.
    tds = soup.find_all('td')
    for tag in tds:
        if(tag.string != None):
            needed_data.append(tag.string)
    for i in range(len(needed_data)):
        needed_data[i] = str(needed_data[i])

    #Populate bid_prices/bid sizes lists.
    index = 0
    while(needed_data[2+index] != 'Price'):
        if(index%2 == 0):
            bid_prices.append(needed_data[2+index])
        else:
            bid_sizes.append(needed_data[2+index])
        index += 1

    #Remove sorted data from needed_data list.
    needed_data = needed_data[index+2:]

    #Populate the ask_prices and ask_sizes lists.
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
    print"_____________________________________________________________"
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
    print now

    #Create session for adding data.
    Session = sessionmaker(bind=engine)
    session = Session()

    #Add bid data into bids table.
    for i in range(len(bid_prices)):
        bid = Bid(cur_time=now, company=company_name, price=bid_prices[i], size=bid_sizes[i])
        session.add(bid)
        session.commit()

    #Add ask data into asks table.
    for i in range(len(ask_sizes)):
        ask = Ask(cur_time=now, company=company_name, price=ask_prices[i], size=ask_sizes[i])
        session.add(ask)
        session.commit()

    #Check if in the database.
    bids = session.query(Bid).filter_by(company = company_name)
    for item in bids:
        print item

    asks = session.query(Ask).filter_by(company = company_name)
    for item in asks:
        print item





