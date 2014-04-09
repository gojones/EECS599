from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Classes needed to interact with SQL database.
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

engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_data')
Base.metadata.create_all(engine)

ticker = raw_input("Please enter the ticker to the company order book you wish to see: ")
ticker = ticker.upper()

bids = session.query(Bid).filter_by(company = ticker)
print "Bids:"
for item in bids:
    print item

print ""

asks = session.query(Ask).filter_by(company = ticker)
print "Asks:"
for item in asks:
    print item


