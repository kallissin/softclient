from flask import Blueprint
from app.controllers.orders_controllers import create_order, create_pdf, delete_order, list_orders, get_order_by_id, get_user_by_order_id, get_technician_by_order_id, get_order_by_status, update_order 


bp = Blueprint('bp_orders', __name__, url_prefix='/orders')

bp.post('')(create_order)
bp.get('')(list_orders)
bp.patch('/<int:id>')(update_order)
bp.get('/<string:order_status>')(get_order_by_status)
bp.get('/<int:id>')(get_order_by_id)
bp.delete('/<int:id>')(delete_order)
bp.get("/<int:order_id>/user")(get_user_by_order_id)
bp.get("/<int:order_id>/technician")(get_technician_by_order_id)
bp.get("/relatory")(create_pdf)