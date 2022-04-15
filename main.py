from flask import Flask, render_template, redirect

from data import db_session

from data.users import User
from data.topics import Topics

import datetime

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from signup_form import RegisterForm
from signin_form import LoginForm
from topic_form import TopicsForm

from add_to_data import add_all_info, work_with_date_users

from sqlalchemy import desc


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/signup', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с такой почтой уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            patronymic=form.pat.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('sign_up.html', title='Регистрация', form=form)



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/signin', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/{user.email}")
        return render_template('sign_in.html', message="Неправильный логин или пароль", form=form)
    return render_template('sign_in.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addquestion', methods=['GET', 'POST'])
@login_required
def addquestion():
    form = TopicsForm()
    if form.validate_on_submit():
        add_all_info(my_db=Topics(), header=form.header.data, content=form.content.data, user_id=current_user.get_id())
        return redirect('/')
    return render_template('question.html', title='Мой вопрос', form=form)


@app.route('/')
def home():
    db_sess = db_session.create_session()
    topics = db_sess.query(Topics).order_by(desc(Topics.created_at)).all()
    user = work_with_date_users(db_sess.query(User).all())
    return render_template('index.html', topics=topics, user=user)


@app.route('/<int:id_topic>/<string:name_topic>')
@login_required
def sometopic(id_topic, name_topic):
    topic = db_session.create_session().query(Topics).filter(Topics.id == id_topic).first()
    return render_template('topic.html', topics=topic)


@app.route('/<string:username>')
@login_required
def profil(username):
    user = db_session.create_session().query(User).filter(User.email == username).first()
    return render_template('user_page.html', person=user)


def main():
    db_session.global_init("db/blogs.db")
    app.run('127.0.0.1', '4000')


if __name__ == '__main__':
    main()