import sys
import os

# Add the parent directory to sys.path to find the 'service' and 'model' modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from service.user_service import UserService
from service.account_service import AccountService
from service.trade_service import TradeService
from model.user import User
from model.account import Account, Type
from model.trade import Trade, CurrencyType, TradeType
from passlib.context import CryptContext


class TestUserService(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def test_register_user(self):
        # Mock user details
        email = "test@example.com"
        password = "password123"
        name = "Test User"

        # Call the service
        user = UserService.register_user(email, password, name, self.db)

        # Assertions
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(self.pwd_context.verify(password, user.password))
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()

    def test_authenticate_user_success(self):
        email = "test@example.com"
        password = "password123"
        hashed_password = self.pwd_context.hash(password)

        # Mocking the database query
        user = User(email=email, password=hashed_password)
        self.db.query(User).filter.return_value.first.return_value = user

        # Call the service
        result = UserService.authenticate_user(email, password, self.db)

        # Assertions
        self.assertIsNotNone(result)
        self.db.query(User).filter.assert_called_once()

    def test_authenticate_user_fail(self):
        email = "test@example.com"
        password = "wrongpassword"

        # Mocking the database query to return None
        self.db.query(User).filter.return_value.first.return_value = None

        # Call the service
        result = UserService.authenticate_user(email, password, self.db)

        # Assertions
        self.assertIsNone(result)


class TestAccountService(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)

    def test_create_account(self):
        user_id = 1
        balance_usd = 1000.0
        balance_btc = 0.1
        account_type = Type.BUY

        # Call the service
        account = AccountService.create_account(user_id, balance_usd, balance_btc, account_type, self.db)

        # Assertions
        self.assertEqual(account.user_id, user_id)
        self.assertEqual(account.balance_usd, balance_usd)
        self.assertEqual(account.balance_btc, balance_btc)
        self.assertEqual(account.type, account_type)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()

    def test_update_account(self):
        account_id = 1
        balance_usd = 2000.0
        balance_btc = 0.2
        account_type = Type.SELL

        # Mock existing account
        account = Account(account_id=account_id, balance_usd=1000.0, balance_btc=0.1, type=Type.BUY)
        self.db.query(Account).filter.return_value.first.return_value = account

        # Call the service
        updated_account = AccountService.update_account(account_id, self.db, balance_usd, balance_btc, account_type)

        # Assertions
        self.assertEqual(updated_account.balance_usd, balance_usd)
        self.assertEqual(updated_account.balance_btc, balance_btc)
        self.assertEqual(updated_account.type, account_type)
        self.db.commit.assert_called_once()

    def test_delete_account(self):
        account_id = 1

        # Mock existing account
        account = Account(account_id=account_id)
        self.db.query(Account).filter.return_value.first.return_value = account

        # Call the service
        result = AccountService.delete_account(account_id, self.db)

        # Assertions
        self.assertTrue(result)
        self.db.delete.assert_called_once_with(account)
        self.db.commit.assert_called_once()

    def test_get_account(self):
        account_id = 1

        # Mock existing account
        account = Account(account_id=account_id)
        self.db.query(Account).filter.return_value.one.return_value = account

        # Call the service
        result = AccountService.get_account(account_id, self.db)

        # Assertions
        self.assertEqual(result.account_id, account_id)
        self.db.query(Account).filter.assert_called_once()


class TestTradeService(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)

    def test_create_trade_buy(self):
        buy_account_id = 1
        sell_account_id = 2
        usd_amount = 100.0
        btc_amount = 0.01
        currency = CurrencyType.USD
        trade_type = TradeType.BUY

        # Mock existing accounts
        buy_account = Account(account_id=buy_account_id, balance_usd=200.0, balance_btc=0.0)
        sell_account = Account(account_id=sell_account_id, balance_usd=0.0, balance_btc=0.1)
        self.db.query(Account).filter.side_effect = [MagicMock(one_or_none=MagicMock(return_value=buy_account)),
                                                     MagicMock(one_or_none=MagicMock(return_value=sell_account))]

        # Call the service
        trade = TradeService.create_trade(buy_account_id, sell_account_id, usd_amount, btc_amount, currency, trade_type, self.db)

        # Assertions
        self.assertEqual(trade.buy_account_id, buy_account_id)
        self.assertEqual(trade.sell_account_id, sell_account_id)
        self.assertEqual(trade.usd_amount, usd_amount)
        self.assertEqual(trade.btc_amount, btc_amount)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()

    def test_get_trade(self):
        trade_id = 1

        # Mock existing trade
        trade = Trade(trade_id=trade_id)
        self.db.query(Trade).filter.return_value.one.return_value = trade

        # Call the service
        result = TradeService.get_trade(trade_id, self.db)

        # Assertions
        self.assertEqual(result.trade_id, trade_id)
        self.db.query(Trade).filter.assert_called_once()

    def test_get_trades_by_account(self):
        account_id = 1

        # Mock existing trades
        trades = [Trade(trade_id=1), Trade(trade_id=2)]
        self.db.query(Trade).filter.return_value.all.return_value = trades

        # Call the service
        result = TradeService.get_trades_by_account(account_id, self.db)

        # Assertions
        self.assertEqual(len(result), 2)
        self.db.query(Trade).filter.assert_called_once()


if __name__ == "__main__":
    unittest.main()
