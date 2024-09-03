from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from model.account import Account
from model.trade import Trade, CurrencyType, TradeType


class TradeService:

    @staticmethod
    def create_trade(buy_account_id: int, sell_account_id: int, usd_amount: float, btc_amount: float,
                     currency: CurrencyType, trade_type: TradeType, db: Session):
        try:
            # Verify that the accounts exist
            buy_account = db.query(Account).filter(Account.account_id == buy_account_id).one_or_none()
            sell_account = db.query(Account).filter(Account.account_id == sell_account_id).one_or_none()

            if not buy_account or not sell_account:
                raise Exception("Invalid account IDs")

            # Verify that the buyer has sufficient balance
            if trade_type == TradeType.BUY:
                if currency == CurrencyType.USD:
                    if buy_account.balance_usd < usd_amount:
                        raise Exception("Insufficient USD balance")
                elif currency == CurrencyType.BTC:
                    if buy_account.balance_btc < btc_amount:
                        raise Exception("Insufficient BTC balance")
            elif trade_type == TradeType.SELL:
                if currency == CurrencyType.USD:
                    if sell_account.balance_usd < usd_amount:
                        raise Exception("Insufficient USD balance in seller's account")
                elif currency == CurrencyType.BTC:
                    if sell_account.balance_btc < btc_amount:
                        raise Exception("Insufficient BTC balance in seller's account")

            # Create the trade record
            trade = Trade(buy_account_id=buy_account_id, sell_account_id=sell_account_id, usd_amount=usd_amount,
                btc_amount=btc_amount, currency=currency, trade_type=trade_type)
            db.add(trade)

            # Handle balance updates based on trade details
            if trade_type == TradeType.BUY:
                if currency == CurrencyType.USD:
                    buy_account.balance_usd -= usd_amount
                    buy_account.balance_btc += btc_amount
                    sell_account.balance_usd += usd_amount
                    sell_account.balance_btc -= btc_amount
                elif currency == CurrencyType.BTC:
                    buy_account.balance_btc -= btc_amount
                    buy_account.balance_usd += usd_amount
                    sell_account.balance_btc += btc_amount
                    sell_account.balance_usd -= usd_amount
            elif trade_type == TradeType.SELL:
                if currency == CurrencyType.USD:
                    buy_account.balance_usd += usd_amount
                    buy_account.balance_btc -= btc_amount
                    sell_account.balance_usd -= usd_amount
                    sell_account.balance_btc += btc_amount
                elif currency == CurrencyType.BTC:
                    buy_account.balance_btc += btc_amount
                    buy_account.balance_usd -= usd_amount
                    sell_account.balance_btc -= btc_amount
                    sell_account.balance_usd += usd_amount

            # Commit the transaction
            db.commit()
            db.refresh(trade)
            return trade
        except Exception as e:
            db.rollback()  # Rollback in case of error
            raise e

    @staticmethod
    def get_trade(trade_id: int, db: Session):
        try:
            trade = db.query(Trade).filter(Trade.trade_id == trade_id).one()
            return trade
        except NoResultFound:
            return None

    @staticmethod
    def get_trades_by_account(account_id: int, db: Session):
        try:
            trades = db.query(Trade).filter(
                (Trade.buy_account_id == account_id) | (Trade.sell_account_id == account_id)).all()
            return trades
        except Exception as e:
            raise e

    @staticmethod
    def get_all_trades(db: Session):
        try:
            trades = db.query(Trade).all()
            return trades
        except Exception as e:
            raise e
