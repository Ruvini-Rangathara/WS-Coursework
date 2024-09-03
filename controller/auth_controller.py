from flask import Blueprint, request, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker

from database import engine
from service.user_service import UserService

# Create a scoped session factory
db_session = scoped_session(sessionmaker(bind=engine))

# Define a blueprint for the auth routes
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    db = db_session()  # Get a new database session

    try:
        user = UserService.register_user(email, password, name, db)
        if not user:
            return jsonify({"detail": "Registration failed"}), 400
        return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201
    except Exception as e:
        db.rollback()  # Rollback in case of error
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session


@auth_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    db = db_session()  # Get a new database session

    try:
        user = UserService.authenticate_user(email, password, db)
        if not user:
            return jsonify({"detail": "Invalid credentials"}), 400
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    except Exception as e:
        db.rollback()  # Rollback in case of error
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()  # Close the session
