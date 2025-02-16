from back.server.server import app, request
from back.controllers import aircraft_controller

@app.route("/get_aircraft_info", methods=["GET"])
def get_aircraft_info():
    
    serial_number = request.args.get('serial_number')
    return aircraft_controller.get_aircraft_by_serial_number(serial_number)