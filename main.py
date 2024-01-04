from flask import Flask, make_response, redirect, request, render_template, url_for
from pysondb import db
from flask_talisman import Talisman
import random

app = Flask(__name__)

Talisman(app, content_security_policy=None)

database = db.getDb('db.json')

@app.route('/api_login', methods=['GET'])
def login():
    login = str(request.args.get('login'))
    password = str(request.args.get('password'))

    user = database.getByQuery({ 'login': login })

    if user == []:
        resp = make_response(render_template('login.html', err="Invalid Login"))
        return resp

    print(user)

    if password == user[0]['password']:
        resp = make_response(redirect(url_for('application')))

        resp.set_cookie('id', str(user[0]['id']))
    else:
        resp = make_response(render_template('login.html', err="Invalid Login"))

    return resp

@app.route('/api_signup', methods=['GET'])
def signup():
    login = str(request.args.get('login'))
    password = str(request.args.get('password'))

    user = database.getByQuery({ 'login': login })
    if user != []:
        return make_response(render_template('signup.html', err="User already exists"))

    user = database.add({
        'login': login,
        'password': password,
        'water': 0,
        'oxygen': 0,
        'podstyle': '',
        'habitants': 0
    })

    resp = make_response(redirect(url_for('onboarding')))
    resp.set_cookie('id', str(user))
    return resp

@app.route('/checkout')
def checkout():
    oxg = int(request.args.get('oxg'))
    wat = int(request.args.get('wat'))
    user = int(request.cookies.get('id'))

    curW = database.getById(user)['water']
    curO = database.getById(user)['oxygen']

    database.updateById(user, {'water': curW + wat, 'oxygen': curO + oxg})

    return redirect(url_for('application'))

@app.route('/set_type')
def set_type():
    idx = int(request.args['idx'])
    typ = request.args['typ']

    database.updateById(idx, {'podstyle': typ})

    return redirect(url_for('habitants'))

@app.route('/set_habitants')
def set_habitants():
    idx = int(request.args['idx'])
    n = int(request.args['n'])

    database.updateById(idx, {'habitants': n, 'oxygen': 40*n, 'water': 80*n})

    return redirect(url_for('application'))

@app.route('/app')
def application():
    user = database.getById(int(request.cookies.get('id')))
    n = round(random.uniform(0.98, 1.2), 5)
    nh = random.randint(44, 49)
    nt = random.randint(70, 74)
    if (user['water'] / (80 * user['habitants']) * 100) < 10:
        low = 'Water'
    elif (user['oxygen'] / (40 * user['habitants']) * 100) < 10:
        low = 'Oxygen'
    else:
        low = None
    return render_template('dashboard.html', user=user, n=n, nh=nh, nt=nt, round=round, low=low)

@app.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

@app.route('/habitants')
def habitants():
    return render_template('habitants.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/')
def landing_page():
    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug=True)
