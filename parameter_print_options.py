from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Class needed to interact with SQL database.
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

engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_data')
Base.metadata.create_all(engine)

#Aquire company ticker.
ticker = raw_input("Please enter the ticker for the company you would like options for: ")
ticker = ticker.upper()

#Aquire strike price (if necessary).
strike = raw_input("Enter strike price to filter (if you want to see all options, enter 0): ")
strike = float(strike)

#Create session needed to query the database.
Session = sessionmaker(bind=engine)
session = Session()

#Query the database for the appropriate options and print them.
if strike == 0:
    options = session.query(Option).filter_by(company = ticker)
else:
    options = session.query(Option).filter_by(company = ticker, strike_price = strike)

for item in options:
    print item


