from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/todo.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column('user_id', db.Integer, primary_key = True)
	username = db.Column('username', db.String(40), unique=True)
	password = db.Column('password', db.String(30))
	email = db.Column('email', db.String(120), unique=True)
	created = db.Column('created', db.DateTime)

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email
		self.created = datetime.utcnow()

	def get_auth(self):
		return True

	def get_active(self):
		return True

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % self.username
