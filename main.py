from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.topics import Topics
import datetime
from flask_login import LoginManager
from signup_form import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('sign_up.html', title='Регистрация', form=form)



# @app.route('/signin', methods=['GET', 'POST'])
# def reqister():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         if form.password.data != form.password_again.data:
#             return render_template('sign_up.html', title='Регистрация',
#                                    form=form,
#                                    message="Пароли не совпадают")
#         db_sess = db_session.create_session()
#         if db_sess.query(User).filter(User.email == form.email.data).first():
#             return render_template('sign_up.html', title='Регистрация',
#                                    form=form,
#                                    message="Пользователь с такой почтой уже есть")
#         user = User(
#             name=form.name.data,
#             surname=form.surname.data,
#             patronymic=form.pat.data,
#             email=form.email.data
#         )
#         user.set_password(form.password.data)
#         db_sess.add(user)
#         db_sess.commit()
#         return redirect('/')
    # return render_template('sign_up.html', title='Регистрация', form=form)


@app.route('/')
def home():
    topics = db_session.create_session().query(Topics).all()
    return render_template('index.html', topics=topics)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()