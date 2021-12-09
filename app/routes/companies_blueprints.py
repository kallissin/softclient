from flask import Blueprint
from app.controllers.companies_controllers import delete_company, get_all, get_one, create_company

bp = Blueprint('db_companies', __name__, url_prefix='/company')

bp.get("")(get_all)
bp.get("/<int:company_id>")(get_one)
bp.delete("/<int:company_id>")(delete_company)
bp.post("")(create_company)
