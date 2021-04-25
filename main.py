import json
from flask_cors import CORS
from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField,SelectField
from wtforms.validators import InputRequired,Email,Length 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user  
from datetime import datetime, timedelta

from models import db, User, Record, Log

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='') 
  Bootstrap(app)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  CORS(app)
  db.init_app(app) 
  
  return app

app = create_app()

app.app_context().push()    

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    diabetic_choices = [(1,"Non-diabetic"),(2,"Pre-diabetic"),(3,"Type1"),(4,"Type2")]

    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    #diabetesType = SelectField('diabetes type', choices = diabetic_choices, validators=[InputRequired()])
''' End Boilerplate Code '''

@app.route('/')
def index():
  return render_template('home.html') 

@app.route('/about')
def index():
  return render_template('about.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password) #diabetesType=form.diabetesType.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('dashboard'))
        #return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard(): 
    return render_template('dashboard.html', name=current_user.username)  

@app.route('/tracker' , methods=['GET','POST'])
@login_required
def tracker():  
    if request.method == 'POST': 
        data = request.form 
        #print(data) 
        bs_logger = Record(userid=current_user.id,bloodsugar = data['BloodSugar'],insulinlevels=data['Insulin'],activity=data['activity'],comments = data['comment']  )
        db.session.add(bs_logger) 
        db.session.commit() 
        return redirect(url_for('dashboard')) 
    else:   
        return render_template('tracker.html', name=current_user.username)  

        
@app.route('/log',methods=['GET'])
@login_required
def readingsLog():  
    userLogs = Record.query.filter_by(userid=current_user.id).all() 
    userLog = []  
    x = {}
    for log in userLogs: 
        date = log.created.date() 
        time = log.created - timedelta(hours=4)
        time = time.strftime("%H:%M")

        x = { 
            "id": log.rid,  
            "date": date,   
            "time": time,  
            "activity": log.activity,
            "bs": log.bloodsugar, 
            "insulin": log.insulinlevels,  
            "comment": log.comments, 
        }
        userLog.append(x)  

    return render_template('log.html', name=current_user.username,logs=userLog)   

@app.route('/log',methods=['GET'])
@login_required
def readingsLog_OneWeek():    
    current_time = datetime.datetime.utcnow()
    one_weeks_ago = current_time - datetime.timedelta(weeks=1)
    userLogs = Record.query.filter_by(userid=current_user.id).filter(created > one_weeks_ago).all() 
    userLog = []  
    x = {}
    for log in userLogs: 
        date = log.created.date() 
        time = log.created - timedelta(hours=4)
        time = time.strftime("%H:%M")

        x = { 
            "id": log.rid,  
            "date": date,   
            "time": time,  
            "activity": log.activity,
            "bs": log.bloodsugar, 
            "insulin": log.insulinlevels,  
            "comment": log.comments, 
        }
        userLog.append(x)  

    return render_template('log.html', name=current_user.username,logs=userLog)  
    
@app.route('/log',methods=['GET'])
@login_required
def readingsLog_TwoWeek():    
    current_time = datetime.datetime.utcnow()
    two_weeks_ago = current_time - datetime.timedelta(weeks=2)
    userLogs = Record.query.filter_by(userid=current_user.id).filter(created > two_weeks_ago).all() 
    userLog = []  
    x = {}
    for log in userLogs: 
        date = log.created.date() 
        time = log.created - timedelta(hours=4)
        time = time.strftime("%H:%M")

        x = { 
            "id": log.rid,  
            "date": date,   
            "time": time,  
            "activity": log.activity,
            "bs": log.bloodsugar, 
            "insulin": log.insulinlevels,  
            "comment": log.comments, 
        }
        userLog.append(x)  

    return render_template('log.html', name=current_user.username,logs=userLog)  
    
@app.route('/log',methods=['GET'])
@login_required
def readingsLog_FourWeek():    
    current_time = datetime.datetime.utcnow()
    four_weeks_ago = current_time - datetime.timedelta(weeks=4)
    userLogs = Record.query.filter_by(userid=current_user.id).filter(created > four_weeks_ago).all() 
    userLog = []  
    x = {}
    for log in userLogs: 
        date = log.created.date() 
        time = log.created - timedelta(hours=4)
        time = time.strftime("%H:%M")

        x = { 
            "id": log.rid,  
            "date": date,   
            "time": time,  
            "activity": log.activity,
            "bs": log.bloodsugar, 
            "insulin": log.insulinlevels,  
            "comment": log.comments, 
        }
        userLog.append(x)  

    return render_template('log.html', name=current_user.username,logs=userLog) 

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)