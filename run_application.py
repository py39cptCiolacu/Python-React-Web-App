import webview
import sqlalchemy
import threading
from sqlalchemy.orm import sessionmaker

from back.settings import DEBUG_MODE, DB_PATH
from back.order.controller import OrderController
from back.material.controller import MaterialController 
from back.aircraft.controller import AircraftController
from back.utils.utils import update_listener


engine = sqlalchemy.create_engine(f"sqlite:///{DB_PATH}", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

controllers = {
    "order": OrderController(db),
    "aircraft": AircraftController(db),
    "material": MaterialController(db)
}

url = "http://localhost:5173" if DEBUG_MODE else "front/dist/index.html"
window = webview.create_window("Demo application", url=url, width=1200)
for controller in controllers.values():
    controller.window = window

thread = threading.Thread(target=update_listener, args=(window, controllers))
thread.start()

webview.start(debug=DEBUG_MODE)
