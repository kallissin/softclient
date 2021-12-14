from flask import Blueprint

from app.controllers.owner_controllers import create_owner, get_all_owner, login

bp = Blueprint('owners', __name__, url_prefix='/owner')


bp.post("")(create_owner)
bp.get("")(get_all_owner)
bp.post('/login')(login)