from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
import requests
import datetime

#Class for interaction with last_trade table
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

#Begin for-loop for scraping last_trade data
for i in range(len(company_lst)):
    company_name = company_lst[i]

    #Set up the BeautifulSoup object needed to scrape data.
    url = "http://finance.yahoo.com/q/ecn?s="+company_name+"+Order+Book"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    #Create list used for storing scraped data.
    needed_data = []

    #Populate the needed_data list
    for tag in soup.find_all('td'):
        if(tag.string != None):
            needed_data.append(tag.string)

    #Create index for while loop.
    index = 0

    if(len(needed_data) > 9):
        #Find last trade index
        while(needed_data[index] != 'Last Trade:'):
            index += 1

        #Put last trade value and last trade time into their own variables.
        last_trade_val = float(needed_data[index+1])
        last_trade_time = needed_data[index+3]

        #Print stuff for checking
        '''print "Company: "
            print company_name
            print "Last Trade: "+str(last_trade_val)
            print "Time: "+last_trade_time'''

        #Create sample last_trade
        trade = LastTrade(cur_time=now, company=company_name, trade_val=last_trade_val, trade_time=last_trade_time)

        #Add sample last_trade into database
        Session = sessionmaker(bind=engine)
        session = Session()

        session.add(trade)
        session.commit()

#Check if it is in the database.
'''trade = session.query(LastTrade).filter_by(company = company_name).first()

print trade.cur_time
print trade.company
print trade.trade_val
print trade.trade_time'''

