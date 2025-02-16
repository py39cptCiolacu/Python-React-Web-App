from flask import request, jsonify, Blueprint

from back.controllers import aircraft_controller, material_controller, order_controller

upload_blueprint = Blueprint("upload", __name__)

@upload_blueprint.route("/upload/<tab_name>", methods=['POST'])
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
    