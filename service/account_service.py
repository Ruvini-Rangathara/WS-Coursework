from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from model.account import Account, Type

class AccountService:

    @staticmethod
    def create_account(user_id: int, balance_usd: float, balance_btc: float, account_type: Type, db: Session):
        account = Account(user_id=user_id, balance_usd=balance_usd, balance_btc=balance_btc, type=account_type)
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def get_account(account_id: int, db: Session):
        try:
            account = db.query(Account).filter(Account.account_id == account_id).one()
            return account
        except NoResultFound:
            return None

    @staticmethod
    def update_account(account_id: int, db: Session, balance_usd: float = None, balance_btc: float = None, account_type: Type = None):
        account = db.query(Account).filter(Account.account_id == account_id).first()
        if account:
            if balance_usd is not None:
                account.balance_usd = balance_usd
            if balance_btc is not None:
                account.balance_btc = balance_btc
            if account_type is not None:
                account.type = account_type
            db.commit()
            db.refresh(account)
            return account
        return None

    @staticmethod
    def delete_account(account_id: int, db: Session):
        account = db.query(Account).filter(Account.account_id == account_id).first()
        if account:
            db.delete(account)
            db.commit()
            return True
        return False

    @staticmethod
    def get_accounts_by_user(user_id: int, db: Session):
        accounts = db.query(Account).filter(Account.user_id == user_id).all()
        return accounts
