#importing all needed packages

from sqlalchemy import create_engine, Column, Text, Integer, Date, Boolean, ForeignKey
from sqlalchemy import case, func, join, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
import pandas as pd
import datetime


# creating the tables for the database

# Starting an engine for the database, which the Session will use for connection
# resources
engine = create_engine('sqlite:///database.db')
engine.connect() 

Base = declarative_base() 

# Define models
# Create and initialize Office, Agent, House, Sales, Seller, Buyer and Commission objects

# Four Base Tables 

class Office(Base):
    """
        This class represents features of each global office and initializes the office's id and location.
    """
    __tablename__ = 'office'
    id = Column(Integer, primary_key = True)
    location = Column(Text, index = True)

    def __repr__(self):
        return "<Office: (id={0}, location={1})".format(self.id, self.location)

class Agent(Base):
    """
        This class represents features of each estate agent and initializes the agent's id and  full name.
    """
    __tablename__ = 'agents'
    id = Column(Integer, primary_key = True)
    first_name = Column(Text, index = True)
    last_name = Column(Text, index = True)
    email = Column(Text, index= True)
    
    def __repr__(self):
        return "<Buyer(id={0}, first_name={1}, last_name={2})".format(self.id, self.first_name, self.last_name, self.email)

    
class Seller(Base):
    """
        This class represents features of real estate seller for the given franchise and initializes the seller's id and full name.
    """
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key = True)
    first_name = Column(Text, index = True)
    last_name = Column(Text, index = True)
    
    def __repr__(self):
        return "<Seller(id={0}, first_name={1}, last_name={2})".format(self.id, self.first_name, self.last_name)


class Buyer(Base):
    """
        This class represents features of real estate buyers from the given franchise and initializes the buyer's id and full name.
    """
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key = True)
    first_name = Column(Text, index = True)
    last_name = Column(Text, index = True)
    
    def __repr__(self):
        return "<Buyer(id={0}, first_name={1}, last_name={2})".format(self.id, self.first_name, self.last_name)

# Additional tables for House information, sale and Comission 

class House(Base):
    """
        This class represents features of real estate in the given franchise and :
        1. Initializes the house's id, name, number of bedrooms/bathrooms, price, zipcode, and status of house;
        2. Connects the house to office id, seller id, and agent id.
    """
    __tablename__ = 'houses'
    id = Column(Integer, primary_key = True)
    name = Column(Text)
    office_id = Column(Integer, ForeignKey('office.id'))
    agent_id = Column(Integer, ForeignKey('agents.id'))
    seller_id = Column(Integer, ForeignKey('sellers.id'))    
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    zipcode = Column(Integer)
    date = Column(Date)
    sold = Column(Boolean)

    def __repr__(self):
        return "<House(id={0}, name={1}, sold={2})>".format(self.id, self.name, self.sold)

class Sale(Base):
    """
        This class represents features of real estate sale for the given franchise and 
        1. Initializes the sale's id,price and date;
        2. Conncets the sale to the house and buyer's id.
    """
    __tablename__ = 'sales'
    id = Column(Integer, primary_key = True)
    house_id = Column(Integer, ForeignKey('houses.id'))
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    sale_price = Column(Integer)
    sale_date = Column(Date)
    
    def __repr__(self):
        return "<Sale(id={0}, house_id={1}, buyer_id={2})>".format(self.id, self.house_id, self.buyer_id)
    

class Commission(Base):
    """
        This class represents features of each commision from selling a house and 
        1. Initializes the commission's id and comission earning;
        2. Connects the comission to the agent id who sold it and sale's id.
    """
    __tablename__ = 'commissions'
    id = Column(Integer, primary_key = True)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    sale_id = Column(Integer, ForeignKey('sales.id'))
    commission = Column(Integer)
    
    def __repr__(self):
        return "<Commission(id={0}, agent_id={1}, commission={2})>".format(self.id, self.agent_id, self.commission)


