from flask import Blueprint
from app.routes.companies_blueprints import bp as bp_companies
from app.routes.users_blueprints import bp as bp_users
from app.routes.technicians_blueprints import bp_technicians
from app.routes.orders_blueprints import bp as bp_orders
from app.routes.owner_blueprints import bp as bp_owners

bp_api = Blueprint('bp_api', __name__, url_prefix='/api')

bp_api.register_blueprint(bp_technicians)
bp_api.register_blueprint(bp_companies)
bp_api.register_blueprint(bp_users)
bp_api.register_blueprint(bp_orders)
bp_api.register_blueprint(bp_owners)
