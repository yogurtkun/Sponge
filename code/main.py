from google.appengine.ext import vendor
vendor.add('lib')

from flask import Flask, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import config
import db_connect


app = Flask(__name__)
app.config.from_object(config)

# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='dummy_region',
#     aws_access_key_id='dummy_access_key',
#     aws_secret_access_key='dummy_secret_key',
#     verify=False)

def connect_db():
    with app.app_context():
        db = SQLAlchemy()
        app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        db.init_app(app)
        result = db.session.execute("SELECT * From test").fetchone()
        db.session.close()
        return str(result)


@app.route('/')
def index():
    return "Hello, World (lets see how long a change takes III)!"


'''
The signup page
'''
@app.route('/signup')
def signup():
    return render_template("signup.html")


'''
New user signup
'''
@app.route('/newUser', methods=['POST'])
def newUser():
	username = str(request.form['username'])
	email = str(request.form['email'])
	password = str(request.form['password'])
	zipcode = str(request.form['zipcode'])
	res = db_connect.newUser(username, email, password, zipcode)
	if res: # signup successful
		session['logged_in'] = True
		session['username'] = username
		return redirect('/')		
	else:
		return render_template("signup.html", error="User exists!")


'''
The login page
'''
@app.route('/login')
def login():
	return render_template("login.html")


'''
User login
'''
@app.route('/userLogin', methods=['POST'])
def userLogin():
	username = str(request.form['username'])
	password = str(request.form['password'])
	table = db_connect.userTable()
	usr = table.find(username, password)
	if usr:
		session['logged_in'] = True
		session['username'] = username
		return redirect('/')
	else:
		return render_template('login.html', error="Invalid username or password")



if __name__ == '__main__':
    app.run(debug=True)
