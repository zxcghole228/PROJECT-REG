import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Image(SqlAlchemyBase):
    __tablename__ = 'images'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    data = sqlalchemy.Column(sqlalchemy.BLOB)
    attract_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey('attractions.id'))
    attract = orm.relation('Attractions')