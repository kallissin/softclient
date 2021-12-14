from flask import Blueprint

from app.controllers.users_controllers import create_user, get_all_users, get_company_by_user_id, get_orders_by_user_id, get_user_by_id, get_user_by_name, login, update_user

bp = Blueprint("bp_users", __name__, url_prefix="/user")

bp.post("")(create_user)
bp.get("")(get_all_users)
bp.get("/<int:user_id>")(get_user_by_id)
bp.get("<string:user_name>")(get_user_by_name)
bp.patch("/<int:user_id>")(update_user)
bp.get("/<int:user_id>/company")(get_company_by_user_id)
bp.get("/<int:user_id>/order")(get_orders_by_user_id)
bp.post("/login")(login)