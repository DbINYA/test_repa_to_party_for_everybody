from views import *
from flask import Flask
from flask_avatars import Avatars
from flask_login import LoginManager
from data.topics import Topics


seck = open('SECRET_KEY.txt', 'r').read()

app = Flask(__name__)
avatars = Avatars(app)
app.config['SECRET_KEY'] = seck
app.config['DEBUG'] = True


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


app.jinja_env.globals.update(decode_img=decode_img)
app.jinja_env.globals.update(get_user=get_user)

app.add_url_rule('/homeforum/<string:lang>/<string:search>/', view_func=home, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/<string:lang>/', view_func=home, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/<string:lang>/<int:page>/<string:search>/', view_func=home, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/<string:lang>/signup/', view_func=register, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/<string:lang>/signin/', view_func=login, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/signout/', view_func=logout)
app.add_url_rule('/homeforum/<string:lang>/addquestion/', view_func=addquestion, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/<string:lang>/topic/<int:id_topic>/to/<string:name_topic>/', view_func=sometopic, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/<string:lang>/video/<int:id_video>/to/<string:title>/', view_func=somevideo, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/<string:lang>/profile/<string:username_id>/', view_func=profil)
app.add_url_rule('/homeforum/<string:lang>/edit/<string:username_id>/', view_func=profile_edit, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/<string:lang>/admin/', view_func=admin, methods=['GET', 'POST'])

app.add_url_rule('/homeforum/<string:search>/', view_func=home, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/', view_func=home, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/<int:page>/<string:search>/', view_func=home, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/addquestion/', view_func=addquestion, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/topic/<int:id_topic>/to/<string:name_topic>/', view_func=sometopic, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/video/<int:id_video>/to/<string:title>/', view_func=somevideo, methods=['GET', 'POST'])
app.add_url_rule('/homeforum/profile/<string:username_id>/', view_func=profil)
app.add_url_rule('/homeforum/admin/', view_func=admin, methods=['GET', 'POST'])


def main():
    db_session.global_init("db/blogs.db")
    app.run('127.0.0.1', '7000')


if __name__ == '__main__':
    main()