from flask import Flask, make_response, redirect, request, render_template, url_for
from pysondb import db

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
            'water': 80,
            'oxygen': 40,
            'energy': 0
        })
    else:
        user = user[0]['id']

    resp = make_response(redirect(url_for('application')))

    resp.set_cookie('id', str(user))

    return resp

@app.route('/app')
def application():
    user = database.getById(int(request.cookies.get('id')))
    return render_template('dashboard.html', user=user)

@app.route('/login')
def login_page():
    return render_template('login.html')

if __name__ == '__main__':
   app.run(debug=True)
