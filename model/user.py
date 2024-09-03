from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    accounts = relationship("Account", back_populates="user")

    #  Define relationships for trades
    # bought_trades = relationship("Trade", foreign_keys="Trade.buyer_id", back_populates="buyer")
    # sold_trades = relationship("Trade", foreign_keys="Trade.seller_id", back_populates="seller")

    # Example method to serialize the user object
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat()  # Convert datetime to ISO format string
        }
