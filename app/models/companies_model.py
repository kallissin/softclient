from app.configs.database import db
from sqlalchemy import Column, String, Integer
from dataclasses import dataclass

@dataclass
class CompanyModel(db.Model):

    id: int
    cnpj: str
    trading_name: str
    company_name: str
    key_id: str

    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    cnpj = Column(String(18), nullable=False)
    trading_name = Column(String, nullable=False, unique=True)
    company_name = Column(String, nullable=False)
    key_id = db.Column(
      db.Integer,
      db.ForeignKey("keys.id"),
      nullable=False,
      unique=True
      )    