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
    usd_amount = Column(Float, nullable=False)
    btc_amount = Column(Float, nullable=False)
    currency = Column(Enum(CurrencyType), nullable=False)
    trade_type = Column(Enum(TradeType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # foreign_keys with column references
    buy_account = relationship("Account", foreign_keys=[buy_account_id], back_populates="buy_trades")
    sell_account = relationship("Account", foreign_keys=[sell_account_id], back_populates="sell_trades")

    def to_dict(self):
        return {
            'trade_id': self.trade_id,
            'buy_account_id': self.buy_account_id,
            'sell_account_id': self.sell_account_id,
            'usd_amount': self.usd_amount,
            'btc_amount': self.btc_amount,
            'currency': self.currency.name,
            'trade_type': self.trade_type.name,
            'created_at': self.created_at.isoformat()
        }

# if currency type is usd and trade type is sell, it means that the user is selling usd to buy btc
# if currency type is btc and trade type is sell, it means that the user is selling btc to buy usd
# if currency type is usd and trade type is buy, it means that the user is buying usd by selling btc
# if currency type is btc and trade type is buy, it means that the user is buying btc by selling usd

# always sell account should be the trade maker
# buy account should be the trade taker
