from flask import Blueprint
from .companies_blueprints import bp as bp_companies


bp_api = Blueprint('bp_api', __name__, url_prefix='/api')
bp_api.register_blueprint(bp_companies)