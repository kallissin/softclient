from flask import Blueprint
from app.controllers.companies_controllers import get_all

bp = Blueprint('db_companies', __name__, url_prefix='/company')

bp.get("")(get_all)