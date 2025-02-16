from back.server.server import app, request
from back.controllers import material_controller

@app.route("/get_material_info", methods=["GET"])
def get_material_info():

    part_number = request.args.get('material_part_number')
    return material_controller.get_material_by_part_number(part_number) 