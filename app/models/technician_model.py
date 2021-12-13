from app.configs.database import db
from sqlalchemy import Column, String, Integer, Date
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class TechnicianModel(db.Model):

    id: int
    name: str
    email: str
    birthdate: str

    __tablename__ = 'technicians'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    birthdate = Column(Date)

    @property
    def password(self):
        raise AttributeError('Password is not acessible.')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
