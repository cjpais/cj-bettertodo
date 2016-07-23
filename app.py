from flask import Flask, render_template
from flask.ext.login import LoginManager
from app_model import db

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('login_template.html')

if __name__ == '__main__':
    app.secret_key = "CHANGE THIS QUICKLY"
    app.run(debug=True, port=8080)
