from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, InputRequired


class AttractForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    number = TextAreaField('Номер в реестре')
    region = TextAreaField('Регион')
    addres = TextAreaField('Адрес')
    categories = SelectField('Категория', coerce=int, validators=[InputRequired()])
    types = SelectField('Вид', coerce=int, validators=[InputRequired()])
    unesko = BooleanField('Юнеско')
    rare_obj = BooleanField('Редкий')
    submit = SubmitField('Применить')