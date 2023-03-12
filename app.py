# importing libraries
from flask import Flask,render_template,request,redirect,url_for

# import flask forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,TextAreaField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import DateField, EmailField, TelField, SubmitField

# library for mails
from flask_mail import Mail, Message

app = Flask(__name__)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rahulsinghpundir89@gmail.com'
app.config['MAIL_PASSWORD'] = 'vlwngnwibrjxlhoc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# object of Mail class
mail = Mail(app)

app.config['SECRET_KEY'] = 'secrety007'


# Login Form class with input fields
class ContactForm(FlaskForm):
    name=StringField(label='Name', id='name', validators=[DataRequired()])
    email = EmailField(label='Email', id='email',validators=[DataRequired(),Email(message="Not valid email.")])
    message=TextAreaField(label='Message',id='message',validators=[DataRequired(),Length(max=500)])
    submit=SubmitField(label='Submit',id='submit')


# Index page or Main page with form
@app.route("/", methods=["GET","POST"])
def index():
    form = ContactForm()
    if request.method == 'POST':
        # Send message to admin by contact form
        msg = Message(
                'Hello from '+request.form['name'],
                sender ='rahulsingpundir89@gmail.com',
                recipients = ['rahulsingpundir85@gmail.com']
               )
        msg.body = request.form['message']
        mail.send(msg)
    return render_template("index.html", form=form)
    

# Project Page
@app.route("/project")
def project():
    return render_template("project.html")


app.run(debug=True)

