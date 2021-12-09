from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from app.configs.database import db
from dataclasses import dataclass
import enum


class MyEnum(enum.Enum):
    aberto = 'aberto'
    em_atendimento = 'em_atendimento'
    fechado = 'fechado'

@dataclass
class OrderModel(db.Model):
    
    id: int
    status: str
    type: float
    description: str
    release_date: str
    update_date: str
    solution: str
    user_id: int
    technician_id: int

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    status = Column(Enum(MyEnum), default="aberto")
    type = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)
    solution = Column(String)
    user_id = Column(Integer, nullable=False)
    technician_id = Column(Integer, nullable=False)