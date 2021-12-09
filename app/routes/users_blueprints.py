# users_blueprints
from flask import Blueprint

from app.controllers.users_controllers import create_user, delete_user, get_all_users, get_company_by_user_id, get_user_by_id, update_user

bp = Blueprint("bp_users", __name__, url_prefix="/user")

bp.post("")(create_user)
bp.get("")(get_all_users)
bp.get("/<int:user_id>")(get_user_by_id)
bp.patch("/<int:user_id>")(update_user)
bp.delete("/<int:user_id>")(delete_user)
bp.get("/<int:user_id>/company")(get_company_by_user_id)