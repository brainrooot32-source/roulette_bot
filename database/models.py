from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True)
    username = Column(String(255), nullable=True)
    stars_balance = Column(Integer, default=0)
    total_spent = Column(Integer, default=0)
    total_won = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

class Spin(Base):
    __tablename__ = "spins"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    cost = Column(Integer, default=25)
    prize_stars = Column(Integer)
    segment_index = Column(Integer)
    telegram_payment_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    telegram_charge_id = Column(String(255), unique=True)
    amount = Column(Integer)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, server_default=func.now())