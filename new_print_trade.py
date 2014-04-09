from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Class needed to interact with SQL database.
Base = declarative_base()

class LastTrade(Base):
    __tablename__ = 'last_trade'
    
    id = Column(Integer, primary_key=True)
    cur_time = Column(String(50))
    company = Column(String(50))
    trade_val = Column(Float)
    trade_time = Column(String(50))
    
    def __repr__(self):
        return "<Last_Trade(date='%s', company='%s', trade_val='%s', trade_time = '%s')>" % (self.cur_time, self.company, self.trade_val, self.trade_time)

engine = create_engine('mysql+mysqldb://gojones26:@localhost/financial_da')
Base.metadata.create_all(engine)

#Create session needed to query the database.
Session = sessionmaker(bind=engine)
session = Session()

#Query the database for last trades, then print them.
last_trades = session.query(LastTrade).all()
for item in last_trades:
    print item




