import sys
import datetime

from flask import Flask, request, make_response, session, render_template, redirect, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session, news_api
from data.db_session import global_init, create_session
from data.jobs import Jobs
from data.login_form import LoginForm
from forms.news import NewsForm
from forms.user import RegisterForm
from data.users import User
from data.news import News
from data.job_form import AddJobForm
from flask_restful import reqparse, abort, Api, Resource
from data import news_resources
from data import users_resources

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# для списка объектов
api.add_resource(news_resources.NewsListResource, '/api/v2/news')

# для одного объекта
api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')

# для списка объектов
api.add_resource(users_resources.UsersListResource, '/api/v2/users')

# для одного объекта
api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()

    return render_template("list_of_lobs.html", jobs=jobs)

@app.route('/odd_even')
def odd_even():
    return render_template('odd_even.html', number=2)


@app.route('/queue')
def queue():
    return render_template('queue.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return redirect('/success')
#     return render_template('login.html', title='Авторизация', form=form)

@app.route('/training/<prof>', methods=['GET', 'POST'])
def training(prof):
    return render_template('training.html', prof=prof)

@app.route('/list_prof/<list>', methods=['GET', 'POST'])
def list_prof(list):
    professions = ['инженер-исследователь',
                   'пилот',
                   'строитель',
                   'экзобиолог',
                   'врач',
                   'инженер по терраформированию',
                   'климатолог',
                   'специалист по радиационной защите',
                   'астрогеолог',
                   'гляциолог',
                   'инженер',
                   'инженер жизнеобеспечения',
                   'метеоролог',
                   'оператор марсохода',
                   'киберинженер',
                   'штурман',
                   'пилот дронов']
    return render_template('professions.html', list=list, professions=professions)

@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    profile = {}
    profile['surname'] = "Whatny"
    profile['name'] = "Pit"
    profile['education'] = "High School"
    profile['profession'] = "штурман"
    profile['sex'] = "Male"
    profile['motivation'] = "None"
    profile['ready'] = "True"
    return render_template('answer.html', title='Анкета', **profile)

@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
            res = make_response(
                f"Вы пришли на эту страницу {visits_count + 1} раз")
            res.set_cookie("visits_count", str(visits_count + 1),
                           max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res

@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register_2.html', title='Регистрация', form=form)


@app.route('/adding_job', methods=['GET', 'POST'])
def adding_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        # jobs = Jobs(
        #     job = form.job.data,
        #     team_leader = form.team_leader.data,
        #     work_size = form.work_size.data,
        #     collaborators = form.collaborators.data,
        #     is_finished = form.is_finished.data)
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.collaborators = form.collaborators.data
        jobs.work_size = form.work_size.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        # db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('adding_job.html', title='Добавление новости',
                           form=form)



@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)

@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = AddJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            form.job.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('adding_job.html',
                           title='Редактирование работы',
                           form=form
                           )

@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )

@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()