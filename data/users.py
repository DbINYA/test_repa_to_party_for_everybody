import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ava_photo = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.String, default='Пользователь', nullable=True) # пользователь-администратор, родитель-эксперт, эксперт


    def __repr__(self):
        return "<User(name='%s', surname='%s', patronymic='%s', email='%s')>" % (self.name, self.surname, self.patronymic, self.email)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)