from flask import Blueprint, request, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker

from database import engine
from model.trade import CurrencyType, TradeType
from service.trade_service import TradeService

# Create a scoped session factory
db_session = scoped_session(sessionmaker(bind=engine))

# Define a blueprint for the trade routes
trade_blueprint = Blueprint('trade', __name__)


@trade_blueprint.route('/add', methods=['POST'])
def create_trade():
    data = request.json
    buy_account_id = data.get('buy_account_id')
    sell_account_id = data.get('sell_account_id')
    usd_amount = data.get('usd_amount')
    btc_amount = data.get('btc_amount')
    currency_str = data.get('currency')
    trade_type_str = data.get('trade_type')

    db = db_session()  # Get a new database session

    try:
        # Validate 'currency' and 'trade_type'
        try:
            currency_enum = CurrencyType[currency_str]
        except KeyError:
            return jsonify({"detail": "Invalid currency type"}), 400

        try:
            trade_type_enum = TradeType[trade_type_str]
        except KeyError:
            return jsonify({"detail": "Invalid trade type"}), 400

        trade = TradeService.create_trade(buy_account_id=buy_account_id, sell_account_id=sell_account_id,
            usd_amount=usd_amount, btc_amount=btc_amount, currency=currency_enum, trade_type=trade_type_enum, db=db)
        return jsonify({"message": "Trade created successfully", "trade": trade.to_dict()}), 201
    except Exception as e:
        db.rollback()  # Rollback in case of error
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session


@trade_blueprint.route('/get/<int:trade_id>', methods=['GET'])
def get_trade(trade_id):
    db = db_session()  # Get a new database session

    try:
        trade = TradeService.get_trade(trade_id, db)
        if not trade:
            return jsonify({"detail": "Trade not found"}), 404
        return jsonify({"trade": trade.to_dict()}), 200
    except Exception as e:
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session


@trade_blueprint.route('/getTradeByAccount/<int:account_id>', methods=['GET'])
def get_trades_by_account(account_id):
    db = db_session()  # Get a new database session

    try:
        trades = TradeService.get_trades_by_account(account_id, db)
        if not trades:
            return jsonify({"detail": "No trades found for the account"}), 404
        return jsonify({"trades": [trade.to_dict() for trade in trades]}), 200
    except Exception as e:
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session


@trade_blueprint.route('/getAll', methods=['GET'])
def get_all_trades():
    db = db_session()  # Get a new database session

    try:
        trades = TradeService.get_all_trades(db)
        return jsonify({"trades": [trade.to_dict() for trade in trades]}), 200
    except Exception as e:
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session
