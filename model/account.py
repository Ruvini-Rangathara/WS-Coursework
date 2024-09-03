from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from model.trade import Trade
from database import Base
import enum


class Type(enum.Enum):
    BUY = 'buy'
    SELL = 'sell'
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'


class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    balance_usd = Column(Float, default=0.0)
    balance_btc = Column(Float, default=0.0)
    type = Column(Enum(Type), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="accounts")
    buy_trades = relationship("Trade", foreign_keys=[Trade.buy_account_id], back_populates="buy_account")
    sell_trades = relationship("Trade", foreign_keys=[Trade.sell_account_id], back_populates="sell_account")

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "user_id": self.user_id,
            "balance_usd": self.balance_usd,
            "balance_btc": self.balance_btc,
            "type": self.type.value,  # Convert enum to string
            "created_at": self.created_at.isoformat(),  # Format datetime to ISO 8601 string
            "updated_at": self.updated_at.isoformat()
        }