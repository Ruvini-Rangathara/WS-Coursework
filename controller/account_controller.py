from flask import Blueprint, request, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker

from database import engine
from service.account_service import AccountService
from model.account import Type  # Import the Type enum

# Create a scoped session factory
db_session = scoped_session(sessionmaker(bind=engine))

# Define a blueprint for the account routes
account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/add', methods=['POST'])
def create_account():
    data = request.json
    user_id = data.get('user_id')
    balance_usd = data.get('balance_usd')
    balance_btc = data.get('balance_btc')
    type_str = data.get('type')

    # Validate 'type'
    try:
        account_type = Type[type_str]  # Convert string to Type enum
    except KeyError:
        return jsonify({"detail": "Invalid account type"}), 400

    db = db_session()  # Get a new database session

    try:
        account = AccountService.create_account(user_id, balance_usd, balance_btc, account_type, db)
        return jsonify({"message": "Account created successfully", "account": account.to_dict()}), 201
    except Exception as e:
        db.rollback()  # Rollback in case of error
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session


@account_blueprint.route('/get/<int:account_id>', methods=['GET'])
def get_account(account_id):
    db = db_session()  # Get a new database session

    try:
        account = AccountService.get_account(account_id, db)
        if not account:
            return jsonify({"detail": "Account not found"}), 404
        return jsonify({"account": account.to_dict()}), 200
    except Exception as e:
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session


@account_blueprint.route('/update/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    data = request.json
    balance_usd = data.get('balance_usd')
    balance_btc = data.get('balance_btc')
    type_str = data.get('type')

    # Validate 'type'
    account_type = None
    if type_str:
        try:
            account_type = Type[type_str]  # Convert string to Type enum
        except KeyError:
            return jsonify({"detail": "Invalid account type"}), 400

    db = db_session()  # Get a new database session

    try:
        account = AccountService.update_account(account_id, db, balance_usd, balance_btc, account_type)
        if not account:
            return jsonify({"detail": "Account not found or not updated"}), 404
        return jsonify({"message": "Account updated successfully", "account": account.to_dict()}), 200
    except Exception as e:
        db.rollback()  # Rollback in case of error
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session


@account_blueprint.route('/delete/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    db = db_session()  # Get a new database session

    try:
        success = AccountService.delete_account(account_id, db)
        if not success:
            return jsonify({"detail": "Account not found"}), 404
        return jsonify({"message": "Account deleted successfully"}), 200
    except Exception as e:
        db.rollback()  # Rollback in case of error
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session


@account_blueprint.route('/getByUserId/<int:user_id>', methods=['GET'])
def get_accounts_by_user(user_id):
    db = db_session()  # Get a new database session

    try:
        accounts = AccountService.get_accounts_by_user(user_id, db)
        if not accounts:
            return jsonify({"detail": "No accounts found for the user"}), 404
        return jsonify({"accounts": [account.to_dict() for account in accounts]}), 200
    except Exception as e:
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session
