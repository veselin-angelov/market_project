from functools import wraps

from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, session, g, make_response
# from flask_login import login_required
from user import User
import json

from advertisement import Advertisement

app = Flask(__name__)

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verifyToken(token):
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

# @app.route('/cookie')
# def cookie():
#     resp = make_response(redirect('/'))
#     resp.set_cookie('somecookiename', 'I am cookie')
#     return resp 

@app.route('/')
def index():
    token = request.cookies.get('token')
    return render_template('index.html', advertisements=Advertisement.all(), token=token)


@app.route('/new', methods=['GET', 'POST'])
@require_login
def new_ad():
    if request.method == 'GET':
        return render_template('new_ad.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['title'],
            request.form['description'],
            request.form['price'],
            request.form['date'],
            1,
            0,
            g.user.id #e tocho e te tuka sum mu ebal i maikata
        )
        Advertisement(*values).create()

        return redirect('/')

@app.route('/<int:id>')
def show_advertisement(id):
    token = request.cookies.get('token')
    advertisement = Advertisement.find(id)

    return render_template('advertisement.html', advertisement=advertisement, token=token)


@app.route('/register', methods=["GET", "POST"])
def register():
    token = request.cookies.get('token')
    if not token or not User.verifyToken(token):
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
    else:
        return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    token = request.cookies.get('token')
    if not token or not User.verifyToken(token):
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            # session.pop('user', None)
            data = json.loads(request.data.decode('ascii'))
            email = data['email']
            password = data['password']
            user = User.find(email)
            # cookie = user.cookie()
            if not user or not user.verifyPassword(password):
                return jsonify({'token': None})
            token = user.generateToken()
            return jsonify({'token': token.decode('ascii')})
    else:
        return redirect('/')       


if __name__ == '__main__':
    app.run()      


