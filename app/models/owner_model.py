from app.configs.database import db
from sqlalchemy import Column, String, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass
from sqlalchemy.orm import validates

from app.exceptions.owners_exceptions import KeyRequiredError


@dataclass
class OwnerModel(db.Model):
    list_keys = ['name', 'username', 'password']
    
    id: int
    name: str
    username: str
    role: str


    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default='super')

    @property
    def password(self):
        raise AttributeError('Password is not acessible.')
    
    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)
    
    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

    @classmethod
    def validate_keys(cls, data: dict):
        data_keys = list(data.keys())
        for key in cls.list_keys:
            if key not in data_keys:
                raise KeyRequiredError(data)


    @validates("name", "username", "password")
    def formated_keys(self, key, value):
        if key == 'name':
            value = value.title()
        
        return value