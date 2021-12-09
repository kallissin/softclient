from flask import Blueprint
from app.routes.companies_blueprints import bp as bp_companies
from app.routes.keys_blueprints import bp as bp_keys
from app.routes.technicians_blueprints import bp_technicians


bp_api = Blueprint('bp_api', __name__, url_prefix='/api')

bp_api.register_blueprint(bp_technicians)
bp_api.register_blueprint(bp_companies)
bp_api.register_blueprint(bp_keys)
