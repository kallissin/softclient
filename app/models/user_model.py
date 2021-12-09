from app.configs.database import db
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app.exceptions.users_exceptions import InvalidBirthDateError, KeyTypeError


@dataclass
class UserModel(db.Model):
    id: int
    name: str
    email: str
    birthdate: str
    registration: int
    role: str

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    birthdate = Column(Date)
    registration = Column(Integer, unique=True, nullable=False)
    role = Column(String(150), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    company = relationship("CompanyModel", backref="user", uselist=False)


    @property
    def password(self):
        raise AttributeError('Password is not acessible.')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

    @validates('birthdate')
    def validate_date(self, key, birthdate):

        try:
            _ = datetime.strptime(birthdate, '%d/%m/%Y')
        except ValueError:
            raise InvalidBirthDateError("birthdate must have format: '%d/%m/%Y'")
        
        return birthdate
    
    @staticmethod
    def validate_keys(data: dict):
        list_keys = ["name", "email", "password", "registration", "role", "company_id"]
        for key in list_keys:
            if not key in list(data.keys()):
                raise KeyTypeError(data)