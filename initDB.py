from main import app
from models import db, User

db.create_all(app=app)

print('database initialized!')