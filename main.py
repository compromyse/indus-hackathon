from flask import Flask, make_response, redirect, request, render_template, url_for
from pysondb import db
import random

app = Flask(__name__)

database = db.getDb('db.json')

@app.route('/api_login', methods=['GET'])
def login():
    login = str(request.args.get('login'))
    password = str(request.args.get('password'))

    user = database.getByQuery({
        'login': login,
        'password': password
    })

    if user == []:
        user = database.add({
            'login': login,
            'password': password,
            'water': 0,
            'oxygen': 0,
            'podstyle': '',
            'habitants': 0
        })

        resp = make_response(redirect(url_for('onboarding')))
    else:
        user = user[0]['id']
        resp = make_response(redirect(url_for('application')))

    resp.set_cookie('id', str(user))

    return resp

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
    return render_template('dashboard.html', user=user, n=n, nh=nh, nt=nt)

@app.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

@app.route('/habitants')
def habitants():
    return render_template('habitants.html')

@app.route('/')
def login_page():
    return render_template('login.html')

if __name__ == '__main__':
   app.run(debug=True)
