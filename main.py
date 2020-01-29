from functools import wraps

from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, session, make_response
from user import User
import json

from advertisement import Advertisement

app = Flask(__name__)
app.config["SECRET_KEY"] = "SxOW8IKSGVShQD6BXtQzMA"

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verifyToken(token):
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    token = request.cookies.get('token')
    user_id = session.get("user_id")
    if token:
        username = User.find_name_by_id(user_id)
        return render_template('index.html', advertisements=Advertisement.all(), token=token, username=username)
    else:
        return render_template('index.html', advertisements=Advertisement.all(), token=token)

@app.route('/profile')
def profile():
    token = request.cookies.get('token')
    if token:
        user_id = session.get("user_id")
        username = User.find_name_by_id(user_id)
        return render_template('profile.html', advertisements=Advertisement.sold_ads(user_id), username=username)
    else:
        return redirect('/login')

@app.route('/new', methods=['GET', 'POST'])
def new_ad():
    if request.method == 'GET':
        return render_template('new_ad.html')
    elif request.method == 'POST':
        user_id = session.get("user_id")
        values = (
            None,
            request.form['title'],
            request.form['description'],
            request.form['price'],
            request.form['date'],
            1,
            0,
            user_id
        )
        Advertisement(*values).create()

        return redirect('/')

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_ad(id):
    advertisement = Advertisement.find(id)
    if request.method == "GET":
        return render_template('edit_ad.html', advertisement=advertisement)
    elif request.method == "POST":
        advertisement.title = request.form['title']
        advertisement.description = request.form['description']
        advertisement.price = request.form['price']
        advertisement.date = request.form['date']
        advertisement.save()
        return redirect(url_for('show_advertisement', id = advertisement.id))


@app.route('/<int:id>')
def show_advertisement(id):
    token = request.cookies.get('token')
    advertisement = Advertisement.find(id)
    user_id = session.get("user_id")
    if advertisement.active == 0:
        buyer = Advertisement.buyer_info_by_id(advertisement.buyer_id)
        return render_template('advertisement.html', advertisement=advertisement, token=token, user_id=user_id, buyer=buyer)
    else:
        return render_template('advertisement.html', advertisement=advertisement, token=token, user_id=user_id)

@app.route('/<int:id>/delete', methods=['POST'])
def delete_ad(id):
    advertisement = Advertisement.find(id)
    if advertisement.seller_id == session.get("user_id"):
        advertisement.delete()

    return redirect('/')

@app.route('/<int:id>/buy', methods=['POST'])
def buy_ad(id):
    advertisement = Advertisement.find(id)
    if advertisement.seller_id != session.get("user_id"):
        buyer_id = session.get("user_id")
        advertisement.buy(buyer_id)

    return redirect('/')

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
    if not token:
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            data = json.loads(request.data.decode('ascii'))
            email = data['email']
            password = data['password']
            user = User.find(email)
            if not user or not user.verifyPassword(password):
                return jsonify({'token': None})
            token = user.generateToken()
            session["user_id"] = user.id
            return jsonify({'token': token.decode('ascii')})
    else:
        return redirect('/')

@app.route('/logout', methods=["GET"])
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', expires=0)
    session.pop("user_id")
    return resp

if __name__ == '__main__':
    app.run(debug=True)      
