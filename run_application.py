import webview
import threading
import logging

from back.settings import DEBUG_MODE 
from back.utils.utils import update_listener
from back.server.server import app
from back.controllers import controllers

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  
        logging.FileHandler('app.log', mode='a') 
    ]
)
logging.info("App started")

def run_flask():
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    url = "http://localhost:5173" if DEBUG_MODE else "front/dist/index.html"
    window = webview.create_window("Demo application", url=url, width=1600, height=900)

    for controller in controllers.values():
        controller.window = window

    thread = threading.Thread(target=update_listener, args=(window, controllers))
    thread.start()

    webview.start(debug=DEBUG_MODE)
