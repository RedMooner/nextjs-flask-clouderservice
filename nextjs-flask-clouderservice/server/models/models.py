from datetime import timedelta
from server import db, session, Base
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt


# Create your models here.


class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta
        )
        return token

    def authenticate(email, password):
        user = User.query.filter(User.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception("No user with this password")
        return user

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hash(str(password))
        print(username, email, password)
