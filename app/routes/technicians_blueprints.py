from flask import Blueprint
from app.controllers.technicians_controllers import create_technician, finalize_order, \
        get_orders_by_technician, get_technician_by_id, get_technicians, login, take_order, update_technician


bp_technicians = Blueprint('db_technicians', __name__, url_prefix='/technicians')

bp_technicians.post("")(create_technician)
bp_technicians.post("/login")(login)
bp_technicians.get("")(get_technicians)
bp_technicians.get("/<int:id>")(get_technician_by_id)
bp_technicians.get("/<int:id>/orders")(get_orders_by_technician)
bp_technicians.patch("/<int:id>")(update_technician)
bp_technicians.patch("/take_order/<int:order_id>")(take_order)
bp_technicians.patch("/finalize_order/<int:order_id>")(finalize_order)
