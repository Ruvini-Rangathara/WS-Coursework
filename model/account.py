from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    balance_usd = Column(Float, default=0.0)
    balance_btc = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="accounts")
    buy_trades = relationship("Trade", foreign_keys=[Trade.buy_account_id], back_populates="buy_account")
    sell_trades = relationship("Trade", foreign_keys=[Trade.sell_account_id], back_populates="sell_account")
