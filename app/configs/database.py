from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.technician_model import TechnicianModel
    from app.models.companies_model import CompanyModel
    from app.models.user_model import UserModel
    from app.models.order_model import OrderModel
    from app.models.owner_model import OwnerModel
