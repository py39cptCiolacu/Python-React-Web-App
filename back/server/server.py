from flask import Flask
from flask_cors import CORS
from back.server.order_endpoints import order_blueprint
from back.server.material_endpoints import material_blueprint
from back.server.aircraft_endpoints import aircraft_blueprint
from back.server.upload_endpoints import upload_blueprint

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(order_blueprint)
app.register_blueprint(aircraft_blueprint)
app.register_blueprint(material_blueprint)
app.register_blueprint(upload_blueprint)
