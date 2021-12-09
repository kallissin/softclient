from app.configs.database import db
from sqlalchemy import Column, String, Integer
from dataclasses import dataclass

@dataclass
class CompanyModel(db.Model):

    id: int
    cnpj: str
    trading_name: str
    company_name: str
    username: str
    password: str
    role: str

    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    cnpj = Column(String(18), nullable=False)
    trading_name = Column(String, nullable=False, unique=True)
    company_name = Column(String, nullable=False, unique=True)
    username = Column(String(150), nullable=True)
    password = Column(String, nullable=True)
    role = Column(String(150), nullable=True)
