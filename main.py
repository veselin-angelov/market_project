from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
# from flask_login import login_required
from user import User
import json

from advertisement import Advertisement

app = Flask(__name__)

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return render_template('index.html', advertisements=Advertisement.all())

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
        ) #tuka ne e dovyrsheno values trqq id na seller ot session-a


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

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = json.loads(request.data.decode('ascii'))
        name = data['name']
        password = data['password']
        user = User.find(name)
        if not user or not user.verifyPassword(password):
            return jsonify({'token': None})
        return redirect('/')
        
        
if __name__ == '__main__':
    app.run()      


