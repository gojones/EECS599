from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
'''-------------------------------------------------------------------------------*
    To run PRINT_CURRENT_PRICES.py, make sure the mysql server on your computer is
    running. Type 'python PRINT_CURRENT_PRICES.py' into the command line, then the
    program will print all of the current prices that are stored in the
    current_prices table of finanical_data.
    -- To modify the code to print a more refined set of prices, modify to query 
    in line 36 to filter by more of the characteristics defined in the CurPrice
    class.
*-------------------------------------------------------------------------------'''

#CurPrice class needed to interact with SQL database.
Base = declarative_base()

class CurPrice(Base):
    __tablename__='current_prices'
    
    id = Column(Integer, primary_key=True)
    cur_time = Column(String(50), primary_key=True)
    company = Column(String(50))
    price = Column(Float)
    
    def __repr__(self):
        return "<CurPrice(company='%s', at_time='%s', price='%s')" % ( self.company, self.cur_time, self.size)

#Create engine to access the MySQL database 'financial_data'.
engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_data')
Base.metadata.create_all(engine)

#Create session for interaction with the database using the created engine.
Session = sessionmaker(bind=engine)
session = Session()

#Using the session, query the database for all CurPrice instances, then print them.
prices = session.query(CurPrice).all()
for item in prices:
    print item

