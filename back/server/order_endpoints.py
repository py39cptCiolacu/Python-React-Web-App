import logging
from flask import request, Blueprint
from back.controllers import order_controller

order_blueprint = Blueprint('order', __name__)

@order_blueprint.route("/get_all_orders", methods = ["GET"])
def get_all_orders():
    logging.info("/get_all_orders was called")
    return order_controller.get_all_orders() 