from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    search = StringField('Введите запрос')
    submit = SubmitField('Поиск')