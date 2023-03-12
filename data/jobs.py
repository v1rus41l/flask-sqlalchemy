import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


from sqlalchemy import orm


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=True)
    # user = orm.relationship('User')