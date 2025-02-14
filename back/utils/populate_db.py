import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

import sqlalchemy
from back.settings import DB_PATH
from back.revision.model import Revision
from back.order.model import Order
from back.material.model import Material 
from back.aircraft.model import Aircraft 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def populate_db(session):
    revision = create_revision()
    session.add(revision)

def create_revision():
    revision = Revision(name="test-revision")
    return revision

tables = [
    Revision.__table__,
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

# delete schemes
Base.metadata.drop_all(engine, tables=tables)
# Create schemas
Base.metadata.create_all(engine, tables=tables)
populate_db(session)
session.commit()
session.close()