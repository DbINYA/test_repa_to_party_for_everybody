from flask import Flask, render_template, redirect, request, flash

from base64 import b64encode

import json

from data import db_session

from data.photos import Photos
from data.users import User
from data.topics import Topics
from data.comments import Comments

from search_form import SearchForm
from signin_form import LoginForm
from signup_form import RegisterForm
from topic_form import TopicsForm
from comments_form import CommentsForm
from edit_form import EditForm

import datetime

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from add_to_data import *

from sqlalchemy import desc, or_


FLAG = False
global_lang_of_site = 'RU'
with open('lang_localization.json', 'r', encoding='utf-8') as jsonf:
    list_lang_site = json.load(jsonf)

def decode_img(img):
    return b64encode(img).decode("utf-8")


def get_user(id):
    return db_session.create_session().query(User).filter(User.id == id).first()


def home(lang=global_lang_of_site, page=1, search='None_search_sit%'):
    global_lang_of_site = lang
    form = SearchForm()

    db_sess = db_session.create_session()

    if form.validate_on_submit():
        if form.search.data:
            search = form.search.data 
        else:
            search = 'None_search_sit%'

    if search != 'None_search_sit%':
        tops = db_sess.query(Topics).order_by(desc(Topics.created_at)).filter(or_(Topics.header.like('%' + search + '%'), 
                                                                                  Topics.content.like('%' + search + '%'),
                                                                                  Topics.header.like('%' + search.lower() + '%'), 
                                                                                  Topics.content.like('%' + search.lower() + '%'),
                                                                                  Topics.header.like('%' + search.upper() + '%'), 
                                                                                  Topics.content.like('%' + search.upper() + '%')))
    else:
        tops = db_sess.query(Topics).order_by(desc(Topics.created_at))
    nums_of_page = len(tops.all()) // 5
    if len(tops.all()) % 5 != 0:
        nums_of_page += 1
    number_of_fifth = page // 5
    if page % 5 != 0:
        number_of_fifth += 1
    if nums_of_page <= number_of_fifth * 5:
        starts_page = (number_of_fifth - 1) * 5 + 1
        ends_page = nums_of_page + 1
    else:
        starts_page = (number_of_fifth - 1) * 5 + 1
        ends_page = starts_page + 5

    topics = tops.limit(5).offset(5 * (page - 1))
    user = work_with_date_users(db_sess.query(User).all())

    return render_template('index.html', topics=topics, user=user, 
                           form_search=form, flag=True, nums_page=nums_of_page, 
                           activated_page=page, list_lang_site=list_lang_site, starts_page=starts_page,
                           ends_page=ends_page, lang_now=lang, lang_btn=False, search_now=search)


def register(lang=global_lang_of_site):
    global_lang_of_site = lang
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('sign_up.html', 
                                   title=list_lang_site[lang][4],
                                   form=form,
                                   message=list_lang_site[lang][28],
                                   list_lang_site=list_lang_site, lang_now=lang, lang_btn=True)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('sign_up.html', title=list_lang_site[lang][4],
                                   form=form,
                                   message=list_lang_site[lang][30],
                                   list_lang_site=list_lang_site, lang_now=lang, lang_btn=True)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            patronymic=form.pat.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/homeforum/')
    return render_template('sign_up.html', title=list_lang_site[lang][4], form=form, flag=FLAG,
                           list_lang_site=list_lang_site, lang_now=lang, lang_btn=True)


def login(lang=global_lang_of_site):
    global_lang_of_site = lang
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            if user.role == 'Администратор':
                return redirect("/homeforum/admin/")  # 3e7mmL-tfXeTCVwCcc2ryQ9r4LWzVyZw09yeKLLVLA
            return redirect("/homeforum/")
        return render_template('sign_in.html', 
                               title=list_lang_site[lang][3], 
                               message=list_lang_site[lang][29], form=form,
                               list_lang_site=list_lang_site, lang_now=lang, lang_btn=True)
    return render_template('sign_in.html', title=list_lang_site[lang][3], form=form, flag=FLAG,
                           list_lang_site=list_lang_site, lang_now=lang, lang_btn=True)


@login_required
def logout():
    logout_user()
    return redirect("/homeforum/") 

@login_required
def addquestion(lang=global_lang_of_site):
    global_lang_of_site = lang
    form = TopicsForm()

    files = request.files.getlist('file[]')

    if form.validate_on_submit():
        for file in files:
            if file:
                mimetype = file.content_type
                if mimetype in ['image/jpeg', 'image/png']:

                    top_id = db_session.create_session().execute("SELECT MAX(id) FROM topics").fetchone()[0] + 1
                    image = Photos(photos_url=file.read(), topics_id=top_id)
                    db_sess = db_session.create_session()
                    db_sess.add(image)
                    db_sess.commit()
                else:
                    return render_template('question.html', title=list_lang_site[lang][0], form=form, flag=FLAG,
                                           list_lang_site=list_lang_site, lang_now=lang, lang_btn=False,
                                           wrong_files=True)
        add_all_info(my_db=Topics(), header=form.header.data, content=form.content.data, user_id=current_user.get_id())
        return redirect('/homeforum/')
    return render_template('question.html', title=list_lang_site[lang][0], form=form, flag=FLAG,
                           list_lang_site=list_lang_site, lang_now=lang, lang_btn=False)


@login_required
def sometopic(id_topic, name_topic, lang=global_lang_of_site):
    global_lang_of_site = lang
    form = CommentsForm()
    db_sess = db_session.create_session()

    topic = db_sess.query(Topics).filter(Topics.id == id_topic).first()
    user = work_with_date_users(db_sess.query(User).all())
    comments_to_topic = db_sess.query(Comments).filter(Comments.topics_id == id_topic).all()

    images = db_sess.query(Photos).filter(Photos.topics_id == id_topic).all()
    attach_files = []

    if form.validate_on_submit():
        if form.answer.data:
            comment = Comments(
            content=form.answer.data,
            user_id=current_user.get_id(),
            topics_id=topic.id)
            db_sess.add(comment)
            db_sess.commit()

            comments_to_topic = db_sess.query(Comments).filter(Comments.topics_id == topic.id).all()

            return redirect('/homeforum/' + lang + '/' + str(id_topic) + '/' + name_topic)

    if images:
        for image in images:
            img = b64encode(image.photos_url).decode("utf-8")
            attach_files.append(img)
        return render_template('topic.html', topics=topic, user=user, flag=FLAG, 
                           list_lang_site=list_lang_site, lang_now=lang, form=form,
                           comments_to_topic=comments_to_topic, lang_btn=False, attach_files=attach_files)

    return render_template('topic.html', topics=topic, user=user, flag=FLAG, 
                           list_lang_site=list_lang_site, lang_now=lang, form=form,
                           comments_to_topic=comments_to_topic, lang_btn=False, attach_files=attach_files)


@login_required
def profil(username_id, lang=global_lang_of_site):
    global_lang_of_site = lang
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == username_id).first()
    questions_of_user = db_sess.query(Topics).order_by(desc(Topics.created_at)).filter(Topics.user_id == username_id).all()[:2]
    answers_of_user = db_sess.query(Comments).order_by(desc(Comments.created_at)).filter(Comments.user_id == username_id).all()[:2]
    users_answer_with_keys = work_with_date_topics(db_sess.query(Topics).all())
    return render_template('user_page.html', person=user, flag=FLAG, 
                           list_lang_site=list_lang_site, lang_now=lang, lang_btn=True, 
                           questions_of_user=questions_of_user, answers_of_user=answers_of_user, users_answer_with_keys=users_answer_with_keys)


@login_required
def profile_edit(username_id, lang=global_lang_of_site):
    global_lang_of_site = lang
    form = EditForm()

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == username_id).first()

    if form.validate_on_submit():

        if form.name.data:
            user.name = form.name.data
        if form.surname.data:
            user.surname = form.surname.data
        if form.pat.data:
            user.patronymic = form.pat.data
        if form.about.data:
            user.about = form.about.data

        file = request.files['file']
        if file:
            mimetype = file.content_type
            if mimetype in ['image/jpeg', 'image/png']:
                user.ava_photo = file.read()
            else:
                return render_template('profile_edit.html', person=user, list_lang_site=list_lang_site, lang_now=lang,
                                       form=form, wrong_files=True)

        db_sess.add(user)
        db_sess.commit()
        return redirect('/homeforum/' + lang + '/profile/' + username_id)
    return render_template('profile_edit.html', person=user, list_lang_site=list_lang_site, lang_now=lang, form=form,
                           wrong_files=False)



def admin(lang=global_lang_of_site):
    return render_template('admin.html')

def somevideo(lang=global_lang_of_site):
    pass