import datetime

from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, nullable=True)
parser.add_argument('job', required=True, nullable=True)
parser.add_argument('collaborators', required=True, nullable=True)
parser.add_argument('work_size', required=True, nullable=True)
parser.add_argument('is_finished', required=True, type=bool)
