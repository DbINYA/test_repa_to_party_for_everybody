from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class TopicsForm(FlaskForm):
    header = StringField('Задайте краткий вопрос', validators=[DataRequired()])
    content = TextAreaField('Опишите интересующую вас тему', validators=[DataRequired()])
    submit = SubmitField('Отправить')