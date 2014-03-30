from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
import requests
import datetime

#Class for interaction with last_trade table
Base = declarative_base()

class Option(Base):
    __tablename__ = 'options'

    id = Column(Integer, primary_key=True)
    cur_time = Column(String(50))
    company = Column(String(50))
    type = Column(String(50))
    strike_price = Column(Float)
    bid_price = Column(String(10))
    ask_price = Column(String(10))
    exp = Column(String(50))

    def __repr__(self):
        return "<Option(date='%s', company='%s', type='%s', strike='%s', bid='%s', ask='%s', expires='%s')>" % (
                    self.cur_time, self.company, self.type, self.strike_price, self.bid_price, self.ask_price, self.exp)

#Create table/class for manipulation
engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_data')
Base.metadata.create_all(engine)

#Get current time
now = str(datetime.datetime.now())[:19]

#Get company_lst from options.txt.
file = open('options.txt', 'r')
company_lst = file.readlines()
file.close()

for i in range(len(company_lst)):
    company_lst[i] = company_lst[i][:len(company_lst[i])-1]

#Begin for-loop for scraping option data
for i in range(len(company_lst)):
    company_name = company_lst[i]

    #Set up the BeautifulSoup object needed to scrape data.
    url = "http://finance.yahoo.com/q/op?s="+company_name+"+Options"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    #Create list for storing scraped data
    needed_data = []

    #Populate the needed_data list.
    for tag in soup.find_all('td'):
        if(tag.string != None):
            needed_data.append(tag.string)

    #Get expiration_data for options.
    slice = 0
    if(len(needed_data) > 2):
        date_block = needed_data[2]
        while(date_block[slice] != ','):
            slice += 1

        expiration_date = date_block[slice+2:]

        #Edit needed_data list for data extraction.
        needed_data = needed_data[3:]

        #set index for while loop.
        index = 0

        #Create session needed to communicate with database.
        Session = sessionmaker(bind=engine)
        session = Session()

        #Loop to add Call Options to the database.
        while(needed_data[index] != 'Put Options'):
            cstrike = needed_data[index]
            cbid = needed_data[index+3]
            cask = needed_data[index+4]
            temp = Option(cur_time=now, company=company_name, type='CALL', strike_price=float(cstrike), bid_price=str(cbid), ask_price=str(cask), exp=str(expiration_date))
            session.add(temp)
            index += 7

        #Commit changes to database.
        session.commit()

        #Increment index in order to set up for puts.
        index += 2

        #Loop to add Put Options to the database.
        while(index < (len(needed_data)-10)):
            pstrike = needed_data[index]
            pbid = needed_data[index+3]
            pask = needed_data[index+4]
            temp2 = Option(cur_time=now, company=company_name, type='PUT', strike_price=float(pstrike), bid_price=str(pbid), ask_price=str(pask), exp=str(expiration_date))
            session.add(temp2)
            index += 7

        #Commit changes to database.
        session.commit()
