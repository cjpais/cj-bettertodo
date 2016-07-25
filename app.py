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
    todos = db.relationship('Todo', backref='todos', lazy='dynamic')

    def __init__(self, username, email, password):
		self.username = username
		self.password = generate_password_hash(password)
		self.email = email
		self.created = datetime.utcnow()

    def check_password(self, password):
        return check_password_hash(self.password, password)

	def __repr__(self):
		return '<User %r>' % self.username

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key = True, unique = True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))
    title = db.Column('todo_title', db.String(140))
    content = db.Column('todo_content', db.String(1000))
    column = db.Column('todo_column', db.Integer)
    created = db.Column('todo_created', db.DateTime)
    finished = db.Column('todo_finished', db.Boolean, default = False)
    finishedTime = db.Column('todo_fin_time', db.DateTime)

    def __init__(self, user_id, content, column, title = None):
        self.user_id = user_id
        self.content = content
        self.column = column
        if title != None:
            self.title = title
        self.created = datetime.utcnow()

@app.route('/', methods=['POST', 'GET'])
def index():
    todolist = []
    columnDict = {"current": 1, "week": 2, "backlog": 3}
    if request.method == "POST":
        data = request.json[0]
        column = columnDict.get(request.json[1])
        change_columns(data, column)
    else:
        if not session.get('logged_in'):
            return render_template('login_template.html')
        else:
            user = User.query.filter_by(id = session['userid']).first()
            todolist = user.todos.all()
            print todolist[2].content
    return render_template('home_template.html', todos = todolist)

@app.route('/new/', methods=['POST'])
def new():
    header = request.form['header']
    content = request.form['content'].strip().rstrip()
    column = int(request.form['column'])
    if header == None:
        newTodo = Todo(session['userid'], content, column)
    else:
        newTodo = Todo(session['userid'], content, column, title = header)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        inputUser = str(request.form['inputUsername'])
        inputPass = str(request.form['inputPassword'])
        result = User.query.filter_by(username=inputUser).first()
        valid = result and result.check_password(inputPass)
        if valid:
            session['logged_in'] = True
            session['userid'] = result.id
            #testnewthing = Todo(result.id, "Test content", 1, title = "TEST")
            #db.session.add(testnewthing)
            #db.session.commit()
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
    return index()

def change_columns(data, column):
    """ Given an array of the moved todos, place them in the database with the
        correct columns.
    """
    for todo in data:
        todoChange = Todo.query.filter_by(id=todo).first()
        todoChange.column = column
    db.session.commit()

if __name__ == '__main__':
    app.secret_key = os.urandom(80)
    db.create_all()
    app.run(debug=True, port=8080)
