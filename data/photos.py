import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Photos(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photos_url = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    topics_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"))
    comments_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("comments.id"))

    comments = orm.relationship('Comments')
    topics = orm.relationship('Topics')
