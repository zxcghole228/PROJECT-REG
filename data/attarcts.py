import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Attractions(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'attractions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    region = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    addres = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    categories = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey('category.id'))
    category = orm.relation('Category')
    types = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey('type.id'))
    type = orm.relation('Type')
    Unesko = sqlalchemy.Column(sqlalchemy.Boolean, unique=False, default=True)
    Rare_obj = sqlalchemy.Column(sqlalchemy.Boolean, unique=False, default=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')