from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class CommentsForm(FlaskForm):
    answer = TextAreaField('Ваш ответ')
    submit = SubmitField('Ответить')