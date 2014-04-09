from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests
import datetime

DB_PATH = '/home/ec2-user/EECS599/'

#Current price class for interaction with SQL database.
Base = declarative_base()

class CurPrice(Base):
    __tablename__='current_prices'

    id = Column(Integer, primary_key=True)
    cur_time = Column(String(50), primary_key=True)
    company = Column(String(50))
    price = Column(Float)

    def __repr__(self):
        return "<CurPrice(company='%s', at_time='%s', price='%s')" % ( self.company, self.cur_time, self.size)

#Create table/class if needed.
engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_data')
Base.metadata.create_all(engine)

#Get current time.
now = str(datetime.datetime.now())[:19]

#Get company_lst from options.txt.
file = open(DB_PATH+'option_file.txt','r')
company_lst = file.readlines()
file.close()

for i in range(len(company_lst)):
    company_lst[i] = company_lst[i][:len(company_lst[i])-1]

#Create session for adding data.
Session = sessionmaker(bind=engine)
session = Session()

#Begin for-loop for scraping current_price data.
for i in range(len(company_lst)):
    company_name = company_lst[i]

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

    #Add current price to database.
    price = CurPrice(cur_time=now, company=company_name, price=current_price)
    session.add(price)
    session.commit()

    #Print for checking.
    print "Current Stock price for "+company_name+": "+current_price

