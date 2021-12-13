from app.configs.database import db
from sqlalchemy import Column, String, Integer, Boolean
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class CompanyModel(db.Model):

    id: int
    cnpj: str
    trading_name: str
    company_name: str
    username: str
    role: str

    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    cnpj = Column(String(18), nullable=False)
    trading_name = Column(String, nullable=False, unique=True)
    company_name = Column(String, nullable=False, unique=True)
    username = Column(String(150), nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(150), nullable=True)
    active = Column(Boolean, nullable=False)


    @property
    def password(self):
        raise AttributeError('Password is not acessible.')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)