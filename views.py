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


def home():
    db_sess = db_session.create_session()
    topics = db_sess.query(Topics).order_by(desc(Topics.created_at)).all()
    user = work_with_date_users(db_sess.query(User).all())
    return render_template('index.html', topics=topics, user=user)


def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('sign_up.html', 
                                   title='Регистрация',
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


def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/{user.email}")
        return render_template('sign_in.html', 
                               title='Авторизация', 
                               message="Неправильный логин или пароль", form=form)
    return render_template('sign_in.html', title='Авторизация', form=form)


@login_required
def logout():
    logout_user()
    return redirect("/")


@login_required
def addquestion():
    form = TopicsForm()
    if form.validate_on_submit():
        add_all_info(my_db=Topics(), header=form.header.data, content=form.content.data, user_id=current_user.get_id())
        return redirect('/')
    return render_template('question.html', title='Мой вопрос', form=form)


@login_required
def sometopic(id_topic, name_topic):
    db_sess = db_session.create_session()
    topic = db_sess.query(Topics).filter(Topics.id == id_topic).first()
    user = work_with_date_users(db_sess.query(User).all())
    return render_template('topic.html', topics=topic, user=user)


@login_required
def profil(username):
    user = db_session.create_session().query(User).filter(User.email == username).first()
    return render_template('user_page.html', person=user)


def search(search):
    db_sess = db_session.create_session()
    topics_sorted_by_data = db_sess.query(Topics)
    topics = topics_sorted_by_data.filter(search in Topics.header).all()
    user = work_with_date_users(db_sess.query(User).all())
    return render_template('index.html', topics=topics, user=user)