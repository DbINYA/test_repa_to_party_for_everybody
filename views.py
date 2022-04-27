from flask import Flask, render_template, redirect, request, flash

import json

from data import db_session

from data.photos import Photos
from data.users import User
from data.topics import Topics

from search_form import SearchForm
from signin_form import LoginForm
from signup_form import RegisterForm
from topic_form import TopicsForm

import datetime

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from add_to_data import *

from sqlalchemy import desc


FLAG = False
global_lang_of_site = 'RU'
with open('lang_localization.json', 'r', encoding='utf-8') as jsonf:
    list_lang_site = json.load(jsonf)


def home(lang=global_lang_of_site, page=0):
    global_lang_of_site = lang
    form = SearchForm()

    mini_page_float = True 

    db_sess = db_session.create_session()
    tops = db_sess.query(Topics).order_by(desc(Topics.created_at))
    n = len(tops.all())
    nums_of_page = n // 10
    if n % 10:
        nums_of_page += 1
    topics = tops.limit(10).offset(10 * page)
    user = work_with_date_users(db_sess.query(User).all())


    if form.validate_on_submit():
        if form.search.data:
            mini_page_float = False 
            topics = db_sess.query(Topics).order_by(desc(Topics.created_at)).filter(Topics.header.like('%' + form.search.data + '%')).all()
            user = work_with_date_users(db_sess.query(User).all())

    return render_template('index.html', topics=topics, user=user, 
                           form_search=form, flag=True, page_float=mini_page_float, 
                           nums_page=nums_of_page, activate_page=page, list_lang_site=list_lang_site, 
                           lang_now=lang)


def register(lang=global_lang_of_site):
    global_lang_of_site = lang
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('sign_up.html', 
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   list_lang_site=list_lang_site, lang_now=lang)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с такой почтой уже есть",
                                   list_lang_site=list_lang_site, lang_now=lang)
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
        return redirect('/homeforum/page/0')
    return render_template('sign_up.html', title='Регистрация', form=form, flag=FLAG,
                           list_lang_site=list_lang_site, lang_now=lang)


def login(lang=global_lang_of_site):
    global_lang_of_site = lang
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/homeforum/profile/{user.email}")
        return render_template('sign_in.html', 
                               title='Авторизация', 
                               message="Неправильный логин или пароль", form=form)
    return render_template('sign_in.html', title='Авторизация', form=form, flag=FLAG,
                           list_lang_site=list_lang_site, lang_now=lang)


@login_required
def logout():
    logout_user()
    return redirect("/homeforum/page/0")


@login_required
def addquestion(lang=global_lang_of_site):
    global_lang_of_site = lang
    form = TopicsForm()
    if form.validate_on_submit():
        add_all_info(my_db=Topics(), header=form.header.data, content=form.content.data, user_id=current_user.get_id())
        return redirect('/homeforum/page/0')
    return render_template('question.html', title=list_lang_site[lang][0], form=form, flag=FLAG,
                           list_lang_site=list_lang_site, lang_now=lang)


@login_required
def sometopic(id_topic, name_topic, lang=global_lang_of_site):
    global_lang_of_site = lang
    db_sess = db_session.create_session()
    topic = db_sess.query(Topics).filter(Topics.id == id_topic).first()
    user = work_with_date_users(db_sess.query(User).all())
    return render_template('topic.html', topics=topic, user=user, flag=FLAG, 
                           list_lang_site=list_lang_site, lang_now=lang)


@login_required
def profil(username, lang=global_lang_of_site):
    global_lang_of_site = lang
    user = db_session.create_session().query(User).filter(User.email == username).first()
    return render_template('user_page.html', person=user, flag=FLAG, 
                           list_lang_site=list_lang_site, lang_now=lang)
