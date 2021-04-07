# Real-Estate-Database-Application

In this application, we are building a database system for a large franchised real estate company:
- The company has many offices located all over the country;
- Each office is responsible for selling houses in a particular area;
- Real estate agents can be assigned to one or more of the offices;
- Each house is assigned one office, one seller and one real estate agent.

Additionally, each seller can sell more than one house and each buyer can buy more than one house.

## Structure of app

The directory consists of the following files:

- `__init__.py` - the configuration and initializes the app.
- `models.py`  - connecting the database and the app.
- `requirements.txt` - the required packages for the project.
- `fictious_data.py` - inserts generated data for testing of the app's functionality.
- `transaction.py` - performs a signle transaction to populate the Houses Table and updated selling statuses
- `db_real_estate.ipynb` - Jupyter Notebook containing step-by-step app creation process to provide a more user-friendly experience to run this app. 


## Installation
Follow the instractions bellow to run the app on your local machine or run Jupyter Notebook for better user experince:

1. Create virtual env
```bash
$ python3 -m venv .venv  
```
2. Activate the Virtual Environment
```bash
$ source .venv/bin/activate       # for Linux & macOS
$ env\Scripts\activate            # for Windows
```
3. Install all the requirements
```bash
$ pip3 install -r requirements.txt
```
4. Locate the root directory and run the __init__.py file to start off the app
```bash
$ python3 __init__.py
```



### Usage of data normalization, indices, and transactions.

**Data Normalization**
The created database application consists of four main tables:
1. Office 
2. Agent
3. Seller
4. Buyer 

Additionally, the database has a table "House" consisting of all available houses for sale. Also, two additional tables are created as sales occur: sales and agent's commissions.

Based on the https://www.studytonight.com/dbms/database-normalization.php: 

- **First Normal Form (1NF)**: 
    - Each column in every table encapsulates only one attribute, such as 'id';
    - All entry values in a column are of the dame domain meaning that they have the same type but different data type, such as Column(Text), Column(Integer), Column(Date) and Column(Boolean);
    - All columns have unique names, such as 'bedrooms';
    - The order in which data is stored does not matter: there are no dependencies in the order in which the data is stored.
    
- **Second Normal Form (2NF)**:
    - First Normal Form is satisfied;
    - All the columns are dependent on a unique primary key only;
    - No partial dependencies in our database: columns are only dependent on the primary key;
    - The tables do not have composite keys;
    
- **Third Normal Form (3NF)**:
    - Second Normal Form is satisfied;
    - No transitive dependency: even though the House table needs information about the agents, offices and sellers, it contains only the reference to their id through a unique foreign key which all the information about agents, offices and sellers are stored in the separate tables with the corresponding name. 
    
    
- **Fourth Normal Form (4NF)**:
    - Third Normal Form is satisfied;
    - For each functional dependency ( X → Y ), X is a super Key.
    - No multi-valued dependency as all tables are separated. 


**Indices**

As we are using SQLite, unique key identifiers are automatically indexed and an ordered list of the data within the index's columns are generated. Also, the joins are implemented based on the foreign key constraints using the unique id of another column (so, it is an indexed primary key). Additionally, the covering indexes are implemented for the main four tables since the data in those tables is often looked up. All of the aforementioned ensures efficiency and main requirements are met. Thus, no other additional indices would be significantly impactful on the query performance. 


**Transactions**
To ensure that all necessary edits happening in one go and avoid partial edits in the database, all the updates are wrapped in a single transaction (function): "either all go through, or none go through". For this, SQLAlchemy provides useful features such as  sessionmaker: 
- Adding tasks to the transaction is done using `session.add(entry)` 
- Executed is done using `session.commit()`
However, if there is an error in the transaction, it rolls back to the previous state without adding the new changes and session is closed with `session.close()` and retires. 

We are using transaction whenever the sale of a house is added to the database:
- A single transaction queries results from the database;
- It adds an entry to the Sale table based on the matched House id;
- It adds an entry to the commission table based on the Sale id. 

We use AVID for SQLAlchmey's implementation of transactions:

- **Atomic**: each transaction adds the entry of one single unit of a house sale;
- **Consistent**: changes are not visible until all of the changes have been implemented (although the old version of the tables is available);
- **Isolated**: all updates occur isolated from the database at first which keeps it intact; 
- **Durable**: all transactions remain committed even if the interruptions happen.





