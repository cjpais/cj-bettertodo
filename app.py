from flask import Flask, render_template, redirect, flash, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

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

    def __init__(self, username, email, password):
		self.username = username
		self.password = generate_password_hash(password)
		self.email = email
		self.created = datetime.utcnow()

    def check_password(self, password):
        return check_password_hash(self.password, password)

	def __repr__(self):
		return '<User %r>' % self.username

@app.route('/')
def index():
    db.create_all()
    print "redirected"
    print session
    if not session.get('logged_in'):
        return render_template('login_template.html')
    else:
        return "meantime before index homepage thing"

@app.route('/login/', methods=['POST', 'GET'])
def login():
    print request.method
    #Session = sessionmaker(bind=app.config["SQLALCHEMY_DATABASE_URI"])
    #s = Session()
    if request.method == 'POST':
        inputUser = str(request.form['inputUsername'])
        inputPass = str(request.form['inputPassword'])
        result = User.query.filter_by(username=inputUser).first()
        valid = result and result.check_password(inputPass)
        if valid:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash("WRONG PASSWORD")
            return render_template('login_template.html')
    return render_template('login_template.html')

@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['inputUsername']
        email = request.form['inputEmail']
        passw = request.form['inputPassword']
        newUser = User(user, email, passw)
        db.session.add(newUser)
        db.session.commit()
        users = User.query.all()
        return redirect(url_for('login'))
    return render_template('register_template.html')

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return home()

if __name__ == '__main__':
    app.secret_key = os.urandom(80)
    app.run(debug=True, port=8080)
