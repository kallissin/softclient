from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import backref, relationship
from app.configs.database import db
from dataclasses import dataclass
from app.models.user_model import UserModel
from app.models.technician_model import TechnicianModel
import enum


class EnumStatus(enum.Enum):
    aberto = 'aberto'
    em_atendimento = 'em_atendimento'
    fechado = 'fechado'
    
class EnumType(enum.Enum):
    computador = 'computador'
    notebook = 'notebook'
    impressora = 'impressora'
    nobreak = 'nobreak'

@dataclass
class OrderModel(db.Model):
    
    id: int
    status: str
    type: str
    description: str
    release_date: str
    update_date: str
    solution: str
    user: UserModel

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    status = Column(Enum(EnumStatus), default='aberto')
    type = Column(Enum(EnumType), nullable=False)
    description = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)
    solution = Column(String)
    user_id = Column(
      Integer,
      ForeignKey("users.id"),
      nullable=False
    )
    technician_id = Column(
      Integer,
      ForeignKey("technicians.id")
    )
    
    user = relationship("UserModel", backref="orders", uselist=False)
    

   