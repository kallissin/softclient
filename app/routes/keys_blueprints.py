from flask import Blueprint
from app.controllers.keys_controllers import get_all

bp = Blueprint('db_keys', __name__, url_prefix='/keys')

bp.get("")(get_all)