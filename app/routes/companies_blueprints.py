from flask import Blueprint
from app.controllers.companies_controllers import delete_company, get_all, get_company_users, get_one, create_company, login, update_company

bp = Blueprint('db_companies', __name__, url_prefix='/company')

bp.get("")(get_all)
bp.get("/<int:company_id>")(get_one)
bp.get("<int:company_id>/users")(get_company_users)
bp.post("")(create_company)
bp.post("/login")(login)
bp.patch("<int:company_id>")(update_company)
bp.delete("/<int:company_id>")(delete_company)

