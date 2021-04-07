from models import *

Session = sessionmaker(bind=engine)
session = Session()

session.close()
Base.metadata.drop_all(bind=engine)