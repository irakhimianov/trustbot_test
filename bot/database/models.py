from datetime import datetime

from sqlalchemy import false, Column, BigInteger, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    telegram_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    username = Column(String, nullable=True)
    fio = Column(String)
    phone_number = Column(String)
    is_banned = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_registered = Column(Boolean, default=False)
    registration_date = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f'<USER>: {self.telegram_id} {self.username} {self.fio} {self.phone_number} ' \
               f'{self.is_banned=} {self.is_active=} {self.is_registered=}'
