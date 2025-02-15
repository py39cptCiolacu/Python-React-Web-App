from flask import Flask, request, jsonify
from flask_cors import CORS
from back.aircraft.controller import AircraftController
from back.material.controller import MaterialController
from back.order.controller import OrderController
from back.settings import DB_PATH

from sqlalchemy.orm import sessionmaker
import sqlalchemy

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#==========================================================
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
#==========================================================

@app.route('/upload/<tab_name>', methods=['POST'])
def upload_file(tab_name):

    
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part"})
    
    file = request.files["file"]
    
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"})
    
    try:
        return _handle_upload(tab_name, file)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def _handle_upload(tab_name: str, file) -> dict:

    if tab_name == "aircrafts":
        return aircraft_controller.add_aircrafts_from_file(file)
    elif tab_name == "orders":
        return order_controller.add_orders_from_file(file)
    elif tab_name == "materials":
        return material_controller.add_materials_from_file(file)
    
    return jsonify({"success": False, "error": f"tab {tab_name} is not a valid tab"})