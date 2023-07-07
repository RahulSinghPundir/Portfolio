# importing libraries
from flask import Flask,render_template,request,redirect

# library for mails
from flask_mail import Mail, Message

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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



app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tododata.db'

db = SQLAlchemy(app)
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
# db.create_all()


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

#Mental Health Template Rendering
@app.route("/MentalHealth")
def menatalHealth():
    return render_template("MentalHealth.html")

#To Do List Template Rendering
@app.route("/TodoList", methods=['GET', 'POST'])
def toDoList():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/TodoList")
    
    allTodo = Todo.query.all() 
    return render_template('Todo/Todolist.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/TodoList")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('/Todo/todoupdate.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/TodoList")

@app.route('/FER')
def facialExpressionRecognition():
    return render_template("FacialExpressionRecognition.html")

# Running the app with debug
app.run(debug=True)

