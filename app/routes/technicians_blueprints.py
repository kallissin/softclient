from flask import Blueprint
from app.controllers.technicians_controllers import create_technician, get_all


bp_technicians = Blueprint('db_technicians', __name__, url_prefix='/technicians')

bp_technicians.post("")(create_technician)
bp_technicians.get("")(get_all)