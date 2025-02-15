import webview
import threading
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from back.settings import DEBUG_MODE, DB_PATH
from back.order.controller import OrderController
from back.material.controller import MaterialController 
from back.aircraft.controller import AircraftController
from back.utils.utils import update_listener
from back.server import app
from back.server import controllers


def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Crearea ferestrei webview (frontend React)
    url = "http://localhost:5173" if DEBUG_MODE else "front/dist/index.html"
    window = webview.create_window("Demo application", url=url, width=1600, height=900)

    # Setarea controllerelor pentru ferestrea webview
    for controller in controllers.values():
        controller.window = window

    # Pornirea aplicației pywebview
    thread = threading.Thread(target=update_listener, args=(window, controllers))
    thread.start()

    webview.start(debug=DEBUG_MODE)
