from flask import Flask, make_response, request
from pysondb import db

app = Flask(__name__)

database = db.getDb('db.json')

@app.route('/signup')
def signup():
    user = str(request.args.get('user'))
    passw = str(request.args.get('passw'))

    database.add({
        'user': user,
        'passw': passw
    })

    return 'OK'
 
@app.route('/login')
def login():
    user = str(request.args.get('user'))
    passw = str(request.args.get('passw'))

    resp = make_response()

    resp.set_cookie(
        'id',
        str(database.getByQuery({
            'user': user,
            'passw': passw
        })[0]['id'])
    )

    return resp

@app.route('/dashboard')
def dashboard():
    idx = request.cookies.get('id')
    user = database.getById(int(idx))

    return user['user']

if __name__ == '__main__':
   app.run(debug=True)
