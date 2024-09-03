# services/user_service.py
from model.user import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    @staticmethod
    def register_user(email: str, password: str, name: str, db: Session):
        hashed_password = pwd_context.hash(password)
        user = User(email=email, password=hashed_password, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(email: str, password: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if user and pwd_context.verify(password, user.password):
            return user
        return None
