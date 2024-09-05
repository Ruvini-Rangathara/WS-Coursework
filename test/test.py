import unittest
import requests

BASE_URL = 'http://localhost:5000'  # Adjust this URL according to your API server configuration


class TestCoinbaseService(unittest.TestCase):

    def setUp(self):
        """Set up initial data like user credentials and URLs."""
        self.register_url = f'{BASE_URL}/register'
        self.login_url = f'{BASE_URL}/login'
        self.add_account_url = f'{BASE_URL}/add'
        self.update_account_url = f'{BASE_URL}/update'
        self.add_trade_url = f'{BASE_URL}/addTrade'
        self.get_trade_by_account_url = f'{BASE_URL}/getTradeByAccount'

        # Create a test user data
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'password123',
            'name': 'Test User'
        }

    def test_user_registration(self):
        """Test user registration"""
        response = requests.post(self.register_url, json=self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.text)

    def test_user_login(self):
        """Test user login"""
        response = requests.post(self.login_url, json={
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.text)

    def test_add_account(self):
        """Test adding an account for the user"""
        account_data = {
            'balance_usd': 1000.0,
            'balance_btc': 0.1,
            'type': 'BUY'
        }
        response = requests.post(self.add_account_url, json=account_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Account created successfully', response.text)

        # Save account ID for future tests
        self.account_id = response.json().get('account_id')

    def test_update_account(self):
        """Test updating an existing account"""
        self.test_add_account()  # Ensure the account is created first

        update_data = {
            'balance_usd': 2000.0,
            'balance_btc': 0.2,
            'type': 'SELL'
        }
        response = requests.put(f'{self.update_account_url}/{self.account_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Account updated successfully', response.text)

    def test_add_trade(self):
        """Test creating a trade between accounts"""
        self.test_add_account()  # Ensure the first account exists

        # Create another account for trade purposes
        account_data_2 = {
            'balance_usd': 500.0,
            'balance_btc': 0.05,
            'type': 'SELL'
        }
        response = requests.post(self.add_account_url, json=account_data_2)
        account_id_2 = response.json().get('account_id')

        trade_data = {
            'buy_account_id': self.account_id,
            'sell_account_id': account_id_2,
            'usd_amount': 500.0,
            'btc_amount': 0.05,
            'currency': 'BTC',
            'trade_type': 'BUY'
        }
        response = requests.post(self.add_trade_url, json=trade_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Trade created successfully', response.text)

    def test_get_trades_by_account(self):
        """Test retrieving trades for a specific account"""
        self.test_add_trade()  # Ensure the trade exists

        response = requests.get(f'{self.get_trade_by_account_url}/{self.account_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertGreater(len(response.json()), 0)  # Ensure there's at least one trade


if __name__ == '__main__':
    unittest.main()
