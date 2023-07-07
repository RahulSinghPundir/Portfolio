# import flask forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,TextAreaField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import DateField, EmailField, TelField, SubmitField

# Login Form class with input fields
class ContactForm(FlaskForm):
    name=StringField(label='Name', id='name', validators=[DataRequired()])
    email = EmailField(label='Email', id='email',validators=[DataRequired(),Email(message="Not valid email.")])
    message=TextAreaField(label='Message',id='message',validators=[DataRequired(),Length(max=500)])
    submit=SubmitField(label='Submit',id='submit')