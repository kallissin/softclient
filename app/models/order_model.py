from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.configs.database import db
from dataclasses import dataclass
from app.models.user_model import UserModel
import enum
from datetime import datetime
from app.exceptions.orders_exceptions import KeyTypeError


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
      
    keys_list = ["type", "description", "user_id", "technician_id"]
    
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
    technician = relationship("TechnicianModel", backref="orders", uselist=False)
    
    @classmethod
    def validate(cls, data: dict):
        for key in cls.keys_list:
            if key not in data.keys():
                raise KeyTypeError(data)

    @classmethod
    def check_needed_keys(cls, data: dict):
        new_dict = {key:value for key, value in data.items() if key in cls.keys_list}
        return new_dict


    
    @staticmethod
    def create_order_data(data: dict):
        current_time = datetime.utcnow()
        data['release_date'] = current_time
        data['solution'] = ""
        data['update_date'] = current_time
        return data
    

   