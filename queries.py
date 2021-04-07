from models import *
Session = sessionmaker(bind=engine)
session = Session()

#  Top 5 offices with most sales
print("Q1: Find the top 5 offices with the most sales for that month.")
print("")
top_offices = session.query(
    
    # Extracting required column elements for filtering
    Office.location,
    func.count(House.office_id) # counting the number of sales per office 
    
    

    # Filtering the sales based on the house sold count per office and limiting to 5
     ).join(Sale, Office).filter(House.sold == True).group_by(House.office_id).order_by(func.count(House.office_id).desc()).limit(5)


print('This report is for the month of April.')
print(pd.read_sql(top_offices.statement, session.bind))

print("")
print("Q2: Find the top 5 estate agents who have sold the most (include their contact details and their sales details so that it is easy contact them and congratulate them).")
print("")
# Top 5 estate agents who sold the most 
top_agents = session.query(
    
    # Extracting required column elements for filtering
    Agent.id,
    Agent.first_name,
    Agent.last_name,
    # counting the number of sales per agent
    func.count(House.agent_id)
    # Filtering the sales based on the house sold count per agent and limiting to 5
     ).join(Sale, Agent).filter(House.sold == True).group_by(House.agent_id).order_by(func.count(House.agent_id).desc()).limit(5)

print(pd.read_sql(top_agents.statement, session.bind))





print("")
print("Q3: Calculate the commission that each estate agent must receive and store the results in a separate table.")
print("")

commision_calculator = session.query(
    
    # Extracting required column elements for filtering
    Agent.first_name, 
    Agent.last_name,
    Agent.email,
    Commission.agent_id, 
    Commission.sale_id, 
    
    # Summing the commision earned by agent
    func.sum(Commission.commission)).join(Sale, Agent).group_by(Commission.agent_id)

print(pd.read_sql(commision_calculator.statement, session.bind))


print("")
print("Q4: For all houses that were sold that month, calculate the average number of days that the house was on the market.")
print("")
# importing stats to calculate mean later 
import statistics as stats

# Average number of days a house was on the market
average_market_stay = session.query(
    
    # Extracting required column elements for filtering
    House.name,
    House.date,
    Sale.sale_date
    
    ).join(Sale).filter(House.sold == True).all()

difference_days = [[] for days in average_market_stay]
average_diff = []
# calculating the difference between the date listed and sold for each house
for i, house in enumerate(average_market_stay):
    difference_days[i].append(house[0])
    difference_days[i].append(house[1])
    difference_days[i].append(house[2])
    difference_days[i].append((house[2] - house[1]).days)
    average_diff.append(difference_days[i][-1])


df = pd.DataFrame(difference_days, columns = ['House Name', 'Listing Date', 'Sale Date', 'Number of days on market'])
print('The average number of days that the house was on the market:', round(stats.mean(average_diff),0), 'days during April')
print(df) 



print("")
print("Q5: For all houses that were sold that month, calculate the average selling price.")
print("")
average_selling_price = session.query(
    func.avg(Sale.sale_price)
     ).one()

print('The average selling price:', round(average_selling_price[0],0), 'USD during April')

# showcasing the houses solt during April
sold_houses = session.query(
    # Extracting required column elements for filtering
    House.name,
    Sale.sale_price
    
    ).join(Sale).filter(House.sold == True)
# print the table
print(pd.read_sql(sold_houses.statement, session.bind))

print("")
print("Q6: Find the zip codes with the top 5 average sales prices")
print("")
top_zipcodes = session.query(
    # Extracting required column elements for filtering
    House.zipcode,
    func.avg(House.price)
     ).join(Sale).filter(House.sold == True).group_by(House.zipcode).order_by(func.avg(House.price).desc()).limit(5)

print(pd.read_sql(top_zipcodes.statement, session.bind))