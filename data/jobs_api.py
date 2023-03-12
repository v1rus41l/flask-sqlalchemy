import flask
from flask import jsonify, request

from . import db_session
from .db_session import create_session
from .jobs import Jobs
from .users import User
from .news import News

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict()
                 for item in jobs]
        }
    )

@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict()
        }
    )

@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'collaborators', 'work_size']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs = Jobs(
        id = request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        collaborators=request.json['collaborators'],
        work_size=request.json['work_size']
    )
    db_sess = create_session()
    list_id = []
    for a in db_sess.query(Jobs).all():
        list_id.append(a.id)
    if jobs.id in list_id:
        return jsonify({'error': 'Bad request'})
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})