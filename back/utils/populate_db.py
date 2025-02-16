import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

import sqlalchemy
from back.settings import DB_PATH
from back.models import Aircraft, Material, Order 
from sqlalchemy.ext.declarative import declarative_base
# from back.utils.base import Base

tables = [
    Order.__table__,
    Material.__table__,
    Aircraft.__table__
    ]

#create the DB if is not there
db_dir = os.path.dirname(DB_PATH)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Create session with DB
engine = sqlalchemy.create_engine(f"sqlite:///{DB_PATH}", echo=True)  # connect to database
Session = sqlalchemy.orm.sessionmaker(bind=engine)  # session to work
session = Session()

# # delete schemes
# Base.metadata.drop_all(engine, tables=tables)
# # Create schemas
# Base.metadata.create_all(engine, tables=tables)
# session.close()