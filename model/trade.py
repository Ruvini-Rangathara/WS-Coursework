from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


# Define ENUMs for trade types and currency types
class TradeType(enum.Enum):
    BUY = 'buy'
    SELL = 'sell'


class CurrencyType(enum.Enum):
    BTC = 'BTC'
    USD = 'USD'


class Trade(Base):
    __tablename__ = 'trades'

    trade_id = Column(Integer, primary_key=True, index=True)
    buy_account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    sell_account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=True)
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(Enum(CurrencyType), nullable=False)
    trade_type = Column(Enum(TradeType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # foreign_keys with column references
    buy_account = relationship("Account", foreign_keys=[buy_account_id], back_populates="buy_trades")
    sell_account = relationship("Account", foreign_keys=[sell_account_id], back_populates="sell_trades")
