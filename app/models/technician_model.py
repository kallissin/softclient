from app.configs.database import db
from sqlalchemy import Column, String, Integer, Date
from dataclasses import dataclass


@dataclass
class TechnicianModel(db.Model):

    id: int
    name: str
    email: str
    registration: int
    birthdate: str

    __tablename__ = 'technicians'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    registration = Column(Integer, nullable=False, unique=True)
    birthdate = Column(Date)
