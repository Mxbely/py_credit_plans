from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
import datetime
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    registration_date = Column(DateTime, default=datetime.datetime.now)
