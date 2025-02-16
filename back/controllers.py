import sqlalchemy
from sqlalchemy.orm import sessionmaker

from back.aircraft.controller import AircraftController
from back.material.controller import MaterialController
from back.order.controller import OrderController
from back.settings import DB_PATH

engine = sqlalchemy.create_engine(f"sqlite:///{DB_PATH}", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

aircraft_controller = AircraftController(db)
material_controller = MaterialController(db)
order_controller = OrderController(db)

controllers = {
    "order": order_controller,
    "aircraft": aircraft_controller,
    "material": material_controller
}