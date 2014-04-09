from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Classes needed to interact with SQL database.
Base = declarative_base()

class CurPrice(Base):
    __tablename__='current_prices'
    
    id = Column(Integer, primary_key=True)
    cur_time = Column(String(50), primary_key=True)
    company = Column(String(50))
    price = Column(Float)
    
    def __repr__(self):
        return "<CurPrice(company='%s', at_time='%s', price='%s')" % ( self.company, self.cur_time, self.size)

engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_data')
Base.metadata.create_all(engine)

#Create session needed to query the database.
Session = sessionmaker(bind=engine)
session = Session()

#Query the database for the current prices, then print them.
prices = session.query(CurPrice).all()
for item in prices:
    print item

