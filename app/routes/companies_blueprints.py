# companies_blueprints
from flask import Blueprint

from app.controllers.companies_controllers import get_companies

bp = Blueprint("bp_companies", __name__, url_prefix="/company")

bp.get("")(get_companies)