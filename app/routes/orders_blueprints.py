from flask import Blueprint
from app.controllers.orders_controllers import create_order, delete_order, list_orders, get_order_by_id


bp = Blueprint('bp_orders', __name__, url_prefix='/orders')

bp.post('')(create_order)
bp.get('')(list_orders)
bp.get('/<int:id>')(get_order_by_id)
bp.delete('/<int:id>')(delete_order)