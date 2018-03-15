# from google.appengine.ext import vendor
# vendor.add('lib')

from flask import Flask, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import config
import db
import json

app = Flask(__name__, template_folder="template")
app.config.from_object(config)

with app.app_context():
    db.init_app(app)

# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='dummy_region',
#     aws_access_key_id='dummy_access_key',
#     aws_secret_access_key='dummy_secret_key',
#     verify=False)

def connect_db():
    with app.app_context():
        conn = SQLAlchemy()
        app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        conn.init_app(app)
        result = conn.session.execute("SELECT * From test").fetchone()
        conn.session.close()
        return str(result)


@app.route('/')
def index():
	# print db.registerUser("yz3060", "yz3060@columbia.edu", "1234", "10025")
	# print db.deleteUser("yz3060")
	return render_template("index.html")


'''
The signup page
'''
@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/portal',methods = ['GET'])
def userPortal():
	user_name = request.args.get('name')
	if not session['logged_in'] or not session['username'] == user_name:
		return redirect('/login')
	user = db.searchUser(user_name)
	return render_template("portal.html", user = user)


'''
New user signup
'''
@app.route('/registerUser', methods=['POST'])
def registerUser():
	username = str(request.form['username'])
	email = str(request.form['email'])
	password = str(request.form['password'])
	zipcode = str(request.form['zipcode'])
	res = db.registerUser(username, email, password, zipcode)
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
@app.route('/loginUser', methods=['POST'])
def loginUser():
	username = str(request.form['username'])
	password = str(request.form['password'])
	res = db.loginUser(username, password)
	if res == 1: # login succeed
		session['logged_in'] = True
		session['username'] = username
		return redirect('/')
	elif res == -1: # wrong password
		return render_template("login.html", error="Wrong password!")
	else: # user doesn't exist
		return render_template("login.html", error="User doesn't exist!")


'''
User logout
'''
@app.route('/logout')
def logoutUser():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)
