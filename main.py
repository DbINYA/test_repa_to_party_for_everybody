from views import *
from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


app.add_url_rule('/', view_func=home)
app.add_url_rule('/signup', view_func=register, methods=['GET', 'POST'])
app.add_url_rule('/signin', view_func=login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=logout)
app.add_url_rule('/addquestion', view_func=addquestion, methods=['GET', 'POST'])
app.add_url_rule('/<int:id_topic>/<string:name_topic>', view_func=sometopic)
app.add_url_rule('/<string:username>', view_func=profil)


def main():
    db_session.global_init("db/blogs.db")
    app.run('127.0.0.1', '4000')


if __name__ == '__main__':
    main()