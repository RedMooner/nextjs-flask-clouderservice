from server import db,session, Base

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,auto_increment=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

