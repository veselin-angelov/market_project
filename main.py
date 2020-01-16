from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager
from user import User

app = Flask(__name__)
app.secret_key = 'q4t7w!z%C*F-J@NcRfUjXn2r5u8x/A?D'

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        info = (
            None,
            request.form['email'],
            User.hashPassword(request.form['password']),
            request.form['name'],
            request.form['address'],
            request.form['mobile']
        )
        User(*info).create()

        return redirect('/')

