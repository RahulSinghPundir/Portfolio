# importing libraries
from flask import Flask,render_template,request

# library for mails
from flask_mail import Mail, Message

# Importing inbuilts functions
from contactform import *
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


# Index page or Main page with form
@app.route("/", methods=["GET","POST"])
def index():
    form = ContactForm()
    if request.method == 'POST':
        # Send message to admin by contact form
        msg = Message(
                'Hello from '+request.form['name'],
                sender =request.form['email'],
                recipients = ['rahulsingpundir89@gmail.com']
               )
        msg.body = request.form['message']
        mail.send(msg)
    return render_template("index.html", form=form)
    

# Project Page Template Rendering
@app.route("/project")
def project():
    return render_template("project.html")

#Sentiment Analysis Template Rendering
@app.route("/Sentimentanalysis")
def Sentimentanalysis():
    return render_template("Sentimentanalysis.html")

#Cartoonify Template Rendering
@app.route("/Cartoonconverter")
def Cartoonconverter():
    return render_template("CartoonConverter.html")

# Running the app with debug
app.run(debug=True)

