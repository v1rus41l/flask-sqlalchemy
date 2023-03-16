import datetime

from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, nullable=True)
parser.add_argument('about', required=True, nullable=True)
parser.add_argument('email', required=True, nullable=True)
# parser.add_argument('hashed_password', required=True, nullable=True)
# parser.add_argument('created_date', default=datetime.datetime.now)