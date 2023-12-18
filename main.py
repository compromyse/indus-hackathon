from flask import Flask
from pysondb import db

app = Flask(__name__)

database = db.getDb('db.json')
 
@app.route('/')
def hello_name():
   return 'Hello'
 
if __name__ == '__main__':
   app.run()
