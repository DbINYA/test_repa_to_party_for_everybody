from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired


class EditForm(FlaskForm):
    name = StringField('Имя')
    surname = StringField('Фамилия')
    pat = StringField("Отчество")
    about = TextAreaField('О себе')
    submit = SubmitField('Сохранить')