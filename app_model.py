from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/todo.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('user_id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(40), unique=True)
    email = db.Column('email', db.String(120), unique=True)
    password = db.Column('password', db.String(30))
    created = db.Column('created', db.DateTime)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email
		self.created = datetime.utcnow()

    def is_active(self):
		return True

    def get_id(self):
		return unicode(self.id)

    def is_authenticated(self):
		return self.authenticated

    def is_anonymous(self):
        return False

	def __repr__(self):
		return '<User %r>' % self.username
