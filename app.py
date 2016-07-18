from flask import Flask, render_template
from app_model import db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login_template.html')

if __name__ == '__main__':
    app.secret_key = "CHANGE THIS QUICKLY"
    app.run(debug=True, port=80)
