from flask import Blueprint
from app.controllers.technicians_controllers import create_technician, delete_technician, \
    get_technician_by_id, get_technicians, test, update_technician


bp_technicians = Blueprint('db_technicians', __name__, url_prefix='/technicians')

bp_technicians.post("")(create_technician)
bp_technicians.get("")(get_technicians)
bp_technicians.get("<int:id>")(get_technician_by_id)
bp_technicians.patch("<int:id>")(update_technician)
bp_technicians.delete("<int:id>")(delete_technician)

bp_technicians.get("/test")(test)