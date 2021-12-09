from app.configs.database import db
from sqlalchemy import Column, String, Integer
from dataclasses import dataclass

@dataclass
class KeysModel(db.Model):

    id: int
    key: str

    __tablename__ = 'keys'

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False, unique=False)  