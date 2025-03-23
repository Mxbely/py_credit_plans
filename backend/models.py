import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String, unique=True, index=True, nullable=False)
    registration_date = Column(DateTime, nullable=False)

    credits = relationship("Credit", back_populates="user")


class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    issuance_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)
    actual_return_date = Column(DateTime, nullable=True)
    body = Column(Float, nullable=False)
    percent = Column(Float, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )

    user = relationship("User", back_populates="credits")
    payments = relationship("Payment", back_populates="credit")


class Dictionary(Base):
    __tablename__ = "dictionaries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)

    plans = relationship("Plan", back_populates="category")
    payments = relationship("Payment", back_populates="payment_type")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    period = Column(DateTime, nullable=False)
    sum = Column(Float, nullable=False)
    category_id = Column(
        Integer, ForeignKey("dictionaries.id"), index=True, nullable=False
    )

    category = relationship("Dictionary", back_populates="plans")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sum = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    credit_id = Column(
        Integer,
        ForeignKey("credits.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    type_id = Column(
        Integer,
        ForeignKey("dictionaries.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    credit = relationship("Credit", back_populates="payments")
    payment_type = relationship("Dictionary", back_populates="payments")
