import sqlalchemy
from data.db_session import SqlAlchemyBase


class Type(SqlAlchemyBase):
    __tablename__ = 'type'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)