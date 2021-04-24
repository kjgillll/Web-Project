from flask_sqlalchemy import SQLAlchemy  
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 
from wtforms.validators import InputRequired, Email, Length
db = SQLAlchemy()
import datetime 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))
    records = db.relationship('Record', backref='user', lazy=True)
    
    def toDict(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "records": self.records,
        "password": self.password
      }


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    bloodsugar = db.Column(db.Integer, nullable = False)
    insulinlevels = db.Column(db.Integer, nullable = True)
    comments = db.Column(db.String(255), nullable = True)

    def toDict(self):
        return {
            "id": self.id,
            "userid": self.userid,
            'created': self.created.strftime("%m/%d/%Y, %H:%M:%S"),
            "bloodsugar": self.bloodsugar,
            "insulinlevels": self.insulinlevels,
            "comments": self.comments           
        }

# class Logs(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     studentId =  db.Column(db.Integer, nullable=False)
#     stream = db.Column(db.Integer, nullable=False)
#     created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

#     def toDict(self):
#         return{
#             'id': self.id,
#             'studentId': self.studentId,
#             'stream': self.stream,
#             'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")
#         }




