from models import *

# Generates Data manually for testing

# Generate office data
office_keys = ['id', 'location']
office_values = [
    [1001, 'San Francisco'],
    [1002, 'New York'],
    [1003, 'Los Angeles'],
    [1004, 'Seatlle'],
    [1005, 'Honolulu'],
    [1006, 'Boston'],
    [1007, 'Portland']]


# Generate agent data
agent_keys = ['id', 'first_name', 'last_name', 'email']
agent_values = [
    [2001, 'Nina', 'Hamidli', 'nina@gmail.com'],
    [2002, 'Nikita', 'Koloskov', 'nikita@gmail.com'],
    [2003, 'Kamran', 'Poladov', 'kamran@gmail.com'],
    [2004, 'Marina', 'Berdikhanova', 'marina@gmail.com'],
    [2005, 'Aysel', 'Hamidova', 'aysel@gmail.com'],
    [2006, 'Teddy', 'Hester', 'teddy@gmail.com'],
    [2007, 'Mateus', 'Pitt', 'mateus@gmail.com'],
    [2008, 'Trang', 'Doan', 'trang@gmail.com'],
    [2009, 'Michelle', 'Smith', 'michelle@gmail.com'],
    [2010, 'Daniel', 'Davis', 'daniel@gmail.com']]

# Generate seller data
seller_keys = ['id', 'first_name', 'last_name']
seller_values = [
    [3001, 'William', 'Johnson'],
    [3002, 'Jennie', 'Miller'],
    [3003, 'Josua', 'Garcia'],
    [3004, 'Dokota', 'Brown'],
    [3005, 'Alina', 'Antonova'],
    [3006, 'James', 'Jones'],
    [3007, 'Katie', 'Smith'],
    [3008, 'Alexandra', 'Anderson'],
    [3009, 'Ellie', 'DeSota'],
    [3010, 'Victor', 'Alev']]


# Generate buyers data
buyer_keys = ['id', 'first_name', 'last_name']
buyer_values = [
    [4001, 'Albert', 'Smith'],
    [4002, 'John', 'Rodriguez'],
    [4003, 'Parviz', 'Hamidov'],
    [4004, 'Kamran', 'Poladov'],
    [4005, 'Britani', 'Sanches'],
    [4006, 'Alex', 'Garcia'],
    [4007, 'Smith', 'Lee'],
    [4008, 'Steven', 'Harris'],
    [4009, 'Ben', 'Clark'],
    [4010, 'Harry', 'Lewis'],
    [4011, 'Allie', 'Walker'],
    [4012, 'Emmalynn', 'Thompson']]


# Generatehousing listing 
house_keys = ['id', 'name', 'office_id', 'agent_id', 'seller_id', 'bedrooms', 'bathrooms', 'price',
             'zipcode', 'date', 'sold']
house_values = [
    [5001, 'Condo for Sale', 1001, 2001, 3001, 5, 5, 849000, 92109, datetime.date(2021, 4, 1), False],
    [5002, 'Bi-level House', 1001, 2002, 3001, 3, 2, 995000, 10352, datetime.date(2021, 4, 3), False],
    [5003, 'A cute house', 1002, 2001, 3002, 2, 1, 93400, 24501, datetime.date(2021, 4, 5), False],
    [5004, 'Pink Apartment', 1002, 2002, 3003, 4, 2, 550000, 24506, datetime.date(2021, 1, 7), False],
    [5005, 'A single room condo', 1003, 2003, 3003, 1, 1, 254000, 90192, datetime.date(2021, 4, 9), False],
    [5006, 'Parkside View', 1003, 2003, 3002, 1, 1, 140000, 98103, datetime.date(2021, 4, 11), False],
    [5007, 'Mangellan Villa', 1003, 2003, 3001, 8, 4, 2357000, 11209, datetime.date(2021, 4, 13), False],
    [5008, 'A sea view apartment', 1004, 2008, 3001, 4, 2, 400000, 98101, datetime.date(2021, 4, 15), False],
    [5009, 'Cute smart house', 1004, 2005, 3001, 3, 3, 589000, 97035, datetime.date(2021, 4, 15), False],
    [5010, 'Yellow walls', 1004, 2006, 3001, 4, 5, 787000, 96801, datetime.date(2021, 4, 19), False],
    [5011, 'Student friendly condo', 1004, 2010, 3001, 2, 1, 40000, 20101, datetime.date(2021, 4, 21), False],
    [5012, 'Mission Studio', 1005, 2009, 3001, 3, 3, 987000, 94103, datetime.date(2021, 4, 21), False],
    [5013, 'Hollywood view appartment', 1005, 2010, 3001, 2, 2, 509870, 90008, datetime.date(2021, 4, 25), False],
    [5014, 'Yet another huge house', 1006, 2005, 3003, 5, 3, 795900, 24502, datetime.date(2021, 4, 29), False]]


# Adding new data entries to the database 

# Dropping all the existing tables in the base
Base.metadata.drop_all(bind=engine)

# Adding entries to the session by creating all tables 
Base.metadata.create_all(bind=engine) 

# Starting a session using SQLAlchemy sessionmaker, also in the same scope as the engine
Session = sessionmaker(bind=engine)
session = Session()


keys = [office_keys, house_keys, agent_keys, seller_keys, buyer_keys]
data_values = [office_values, house_values, agent_values, seller_values, buyer_values]
tables = [Office, House, Agent, Seller, Buyer]

def add_new_entries(keys, data_values, tables):
    '''
        This function adds entries to the table using keys, values and table names.
    '''
    temp = []
    for value in data_values:
        dict_temp = dict(zip(keys, value))
        temp.append(dict_temp)
    
    for single_entry in temp:
        entry = tables(**single_entry)
        session.add(entry)

for i in range(len(tables)):
    add_new_entries(keys[i], data_values[i], tables[i])

session.commit()
session.close()


# Showcase the tables

# Office
print('Showing Office Table')
print(pd.read_sql(session.query(Office).statement, session.bind))
print("")
# Agents
print('Showing Agent Table')
print(pd.read_sql(session.query(Agent).statement, session.bind))
print("")
# Sellers
print('Showing Agent Table')
print(pd.read_sql(session.query(Seller).statement, session.bind))
print("")
# Buyers 
print('Showing Agent Table')
print(pd.read_sql(session.query(Buyer).statement, session.bind))
print("")
# House listings
print('Showing Agent Table')
print(pd.read_sql(session.query(House).statement, session.bind))
print("")
