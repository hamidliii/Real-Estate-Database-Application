from models import *

Session = sessionmaker(bind=engine)
session = Session()


def sales(house_id, buyer_id, agent_id,  sale_date):
    ''' 
        This function performs a single transaction:
            1) Addition of a sale entry to a database;
            2) Calculating the comission rate and adding it to the Comission table;
            3) Updating the houses sell status;
            4) Commition of the transaction to the database.
    '''

    #  Quering house price from House table using uqniue house id 
    # .first() - returning first results of the list 
    listing_price = session.query(House.price).filter(House.id == house_id).first()[0]
    
    
    # Calculating agent's commission based on the given rates
    commision_rate = case([(House.price < 100000, 0.01), # For houses sold below $100,000 the commission is 10%
           (House.price < 200000, 0.075), # For houses between $100,000 and $200,000 the commission is 7.5%
           (House.price < 500000, 0.06), # For houses between $200,000 and $500,000 the commission is 6%
           (House.price  < 1000000, 0.05), # For houses between $500,000 and $1,000,000 the commission is 5%
           (House.price  > 1000000, 0.04),]) # For houses above $1,000,000 the commission is 4%
    # Storing the commision for the agent based on comission_rate
    agent_commission = session.query(House.price*commision_rate).filter(House.id == house_id).first()[0]
    
    # Adding Sales table entry to the database 
    sale_entry = Sale( 
        house_id = house_id,
        buyer_id = buyer_id,
        sale_date = sale_date,
        sale_price = listing_price)
    
    # Adding the entry to the session
    session.add(sale_entry)
    
    # Adding Comission table entry to the database 
    sale = session.query(Sale.id).filter(House.id == house_id).first()[0]
    
    commission_entry = Commission(
        agent_id = agent_id,
        sale_id = sale,
        commission = agent_commission)
    
    # add the entry to the session
    session.add(commission_entry)
    
    # Updateding the house status to sold in the House table
    house_sold = session.query(House).filter(House.id == house_id)
    house_sold.update({House.sold: True})

    # commit the transaction
    session.commit()
    
# insert house sales 
sales(5001, 4001, 2001, datetime.date(2021, 4, 10))
sales(5002, 4002, 2002, datetime.date(2021, 4, 19))
sales(5003, 4003, 2001, datetime.date(2021, 4, 27))
sales(5005, 4005, 2003, datetime.date(2021, 4, 25))
sales(5006, 4006, 2003, datetime.date(2021, 4, 28))
sales(5007, 4010, 2003, datetime.date(2021, 4, 19))
sales(5008, 4004, 2008, datetime.date(2021, 4, 18))
sales(5009, 4007, 2005, datetime.date(2021, 4, 22))
sales(5011, 4008, 2010, datetime.date(2021, 4, 25))
sales(5013, 4012, 2010, datetime.date(2021, 4, 30))
sales(5014, 4011, 2005, datetime.date(2021, 4, 30))
    
print("")
print("Updated Sale Table")
# Updated Sales Data
pd.read_sql(session.query(Sale).statement, session.bind)
print("")

print("")
print("Updated Sold Status on House Table after transaction")
# Updated sold status
pd.read_sql(session.query(House).statement, session.bind)
print("")

print("")
print("Updated Commission Table after transaction")
# Updated Commissions Data
pd.read_sql(session.query(Commission).statement, session.bind)
print("")