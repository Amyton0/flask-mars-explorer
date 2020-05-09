from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Departments
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class JobForm(FlaskForm):
    job = StringField('Job', validators=[DataRequired()])
    team_leader = StringField('Team leader (id)', validators=[DataRequired()])
    work_size = IntegerField('Work size (hours)', validators=[DataRequired()])
    collaborators = StringField('Collaborators (id)', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DepartmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    chief = StringField('Chief (id)', validators=[DataRequired()])
    members = StringField('Members (id)', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    users = session.query(User)
    return render_template("index.html", jobs=jobs, User=User, users=users)


@app.route("/departments")
def departments():
    session = db_session.create_session()
    departments = session.query(Departments)
    users = session.query(User)
    return render_template("departments.html", departments=departments, Departments=Departments, users=users, User=User)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
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
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        session.merge(jobs)
        session.commit()
        return redirect('/')
    return render_template('add_job.html', title='Add job', form=form)


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
        if not jobs:
            jobs = session.query(Jobs).filter(Jobs.id == id, current_user.id == 1).first()
        if jobs:
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
        if not jobs:
            jobs = session.query(Jobs).filter(Jobs.id == id, current_user.id == 1).first()
        if jobs:
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            session.merge(jobs)
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html', title='Edit job', form=form)


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == id,
                                      Jobs.team_leader == current_user.id).first()
    if not jobs:
        jobs = session.query(Jobs).filter(Jobs.id == id,
                                          current_user.id == 1).first()
    if jobs:
        session.delete(jobs)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        departments = Departments()
        departments.title = form.title.data
        departments.chief = form.chief.data
        departments.email = form.email.data
        departments.members = form.members.data
        session.merge(departments)
        session.commit()
        return redirect('/departments')
    return render_template('add_department.html', title='Add department', form=form)


@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        session = db_session.create_session()
        departments = session.query(Departments).filter(Departments.id == id, Departments.chief == current_user.id).first()
        if not departments:
            departments = session.query(Departments).filter(Departments.id == id, current_user.id == 1).first()
        if departments:
            departments = Departments()
            departments.title = form.title.data
            departments.chief = form.chief.data
            departments.email = form.email.data
            departments.members = form.members.data
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        departments = session.query(Departments).filter(Departments.id == id,
                                                        Departments.chief == current_user.id).first()
        if not departments:
            departments = session.query(Departments).filter(Departments.id == id, current_user.id == 1).first()
        if departments:
            session = db_session.create_session()
            departments.title = form.title.data
            departments.chief = form.chief.data
            departments.email = form.email.data
            departments.members = form.members.data
            session.merge(departments)
            session.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('add_department.html', title='Edit department', form=form)


@app.route('/delete_department/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    session = db_session.create_session()
    departments = session.query(Departments).filter(Departments.id == id,
                                      Departments.chief == current_user.id).first()
    if not departments:
        departments = session.query(Departments).filter(Departments.id == id,
                                          current_user.id == 1).first()
    if departments:
        session.delete(departments)
        session.commit()
    else:
        abort(404)
    return redirect('/departments')


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
