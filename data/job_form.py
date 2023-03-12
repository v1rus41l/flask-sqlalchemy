from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, IntegerField, StringField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = IntegerField('Team Leader ID', validators=[DataRequired()])
    job = StringField('Job Title', validators=[DataRequired()])
    work_size = IntegerField('Work size in hours', validators=[DataRequired()])
    collaborators = IntegerField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')

    submit = SubmitField('Submit')