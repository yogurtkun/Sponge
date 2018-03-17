from google.appengine.ext import vendor
vendor.add('lib')

import base64

from flask import Flask, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import config
import schema
import json
import account, post

app = Flask(__name__, template_folder="template")
app.config.from_object(config)

with app.app_context():
    schema.init_app(app)


@app.route('/')
def index():
	return render_template("index.html")


'''
The signup page
'''
@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/portal',methods = ['GET'])
def userPortal():
	if not loggedIn():
		return redirect('/login')
	username = session['username']
	user = account.searchUser(username)
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
	res = account.registerUser(username, email, password, zipcode)
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
	res = account.loginUser(username, password)
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

'''
check if there is a logged_in user
'''
def loggedIn():
	return 'logged_in' in session.keys() and session['logged_in']

        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('notFound.html'), 404

'''
Return seller post list
'''
@app.route('/SellerPosts')
def SellerPosts():
	posts = post.searchSellerPosts()
	return render_template("sellerPosts.html", posts)


'''
Return seller post list
'''
@app.route('/BuyerPosts')
def SellPosts():
	posts = post.searchBuyerPosts()
	return render_template("buyerPosts.html", posts)



'''
Page for seller post creating
'''
@app.route('/NewSellerPost')
def createSellerPostPage():
	if not loggedIn():
		return render_template('login.html', error='Please login first')
	return render_template('post.html', seller=True)


'''
Page for buyer post creating
'''
@app.route('/NewBuyerPost')
def createBuyerPostPage():
	if not loggedIn():
		return render_template('login.html', error='Please login first')
	return render_template('post.html', buyer=True)


'''
Create Seller Post
'''
@app.route('/NewSellerPost', methods=['POST'])
def createSellerPost():
	return createPost(request, "Seller")


'''
Create Buyer Post
'''
@app.route('/NewBuyerPost', methods=['POST'])
def createBuyerPost():
	return createPost(request, "Buyer")


'''
Create A Post for Buyer or Seller
'''
def createPost(request, flag):
	if not loggedIn():
		return render_template('login.html', error='Please login first')
	isSeller = flag == "Seller"
	isBuyer = flag == "Buyer"
	title = str(request.form['title'])
	description = str(request.form['description'])
	category = str(request.form['category']) if 'category' in request.form.keys() else None
	price = str(request.form['price']) if 'price' in request.form.keys() and len(request.form['price'])>0 else None
	location = str(request.form['location']) if 'location' in request.form.keys() and len(request.form['location'])>0 else None
	image = request.files.get('image') # None if no such file
	if image == None or image.filename == '':
		image = None
	else:
		image = image.read() # to binary file
	# time = current time, will be calculated in database
	name = session['username']
	postId = post.createPost(title, description, category, price, location, image, name, isSeller, isBuyer)
	if postId == None:
		return render_template('post.html', seller=isSeller, buyer=isBuyer, error='Create post failed!')
	#return render_template('post.html', seller=isSeller, buyer=isBuyer, error='Create post successfully!', postId = postId)
	if isSeller:
		return redirect('/SellerPost?postId=' + str(postId))
	if isBuyer:
		return redirect('/BuyerPost?postId=' + str(postId))



'''
Post List Page
'''
@app.route('/postList')
def postList():
	posts = {}
	posts['SellerPosts'] = post.searchSellerPosts()
	posts['BuyerPosts'] = post.searchBuyerPosts()
	return render_template("postlist.html", posts=posts)




'''
Post Detail Page
'''
@app.route('/SellerPost', methods=['GET'])
def getSellerPost():
	postId = int(request.args['postId'])
	return getPost(postId, "Seller")


@app.route('/BuyerPost', methods=['GET'])
def getBuyerPost():
	postId = int(request.args['postId'])
	return getPost(postId, "Buyer")


def getPost(postId, flag):
	isSeller = flag == "Seller"
	isBuyer = flag == "Buyer"
	postData = post.getPost(postId, isSeller, isBuyer)
	if postData == None:
		if isSeller:
			return redirect('/NewSellerPost')
		if isBuyer:
			return redirect('/NewBuyerPost')
	#print postData
	image = postData['image']
	if image != None:
		newImage = base64.b64encode(image).decode('ascii')
		postData['image'] = newImage
	return render_template("postdetail.html", seller=isSeller, buyer=isBuyer, post=postData)



if __name__ == '__main__':
    app.run(debug=True)
