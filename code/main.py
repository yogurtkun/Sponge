from google.appengine.ext import vendor
vendor.add('lib')

from flask import Flask, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import config
import schema
import json
import account, post, order, review, post_comment, message

app = Flask(__name__, template_folder="template")
app.config.from_object(config)

with app.app_context():
    schema.init_app(app)


@app.route('/')
def index():
    return redirect('/postlist') #render_template("index.html")


'''
The signup page
'''
@app.route('/signup')
def signup():
    return render_template("signup.html")


'''
User portal
'''
@app.route('/portal')
def userPortal():
    if not loggedIn():
        return redirect('/login')
    return render_template("messagebox.html",username = session['username'])


'''
Get user info
'''
@app.route('/userinfo',methods=['POST'])
def userinfo():
    if not loggedIn():
        return redirect('/login')
    username = session['username']
    user = account.searchUser(username)
    return json.dumps(user)

'''
Update user informatin
'''
@app.route('/updateUser', methods=['POST'])
def updateUser():
    update = {key : request.form[key] for key in ('username', 'email', 'zipcode', 'password','phoneNumber','address') if key in request.form}
    user = account.updateUser(update, update['username'])
    if user is None:
        return 'Fail'
    return 'Success'


'''
Retrival posts related to the user
'''
@app.route('/getPostsByUser/<username>', methods=['POST'])
def getPostsByUser(username):
    posts = {}
    posts['SellerPosts'] = post.searchSellerPosts(username=username)
    posts['BuyerPosts'] = post.searchBuyerPosts(username=username)
    return json.dumps(posts)


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
    postId = post.createPost(title, description, category, price, location, image, name, flag)
    if postId == None:
        return render_template('post.html', seller=isSeller, buyer=isBuyer, error='Create post failed!')
    res = account.addPost(name, postId, flag)
    if res == None:
        return render_template('post.html', seller=isSeller, buyer=isBuyer, error='Create post failed!')
    if isSeller:
        return redirect('/SellerPost?postId=' + str(postId))
    if isBuyer:
        return redirect('/BuyerPost?postId=' + str(postId))



'''
Post List Page
'''
@app.route('/postlist')
def postList():
    categories = ['Beauty','Books','Electronics','Clothing','Accessories','Health','Kitchen','Music','Software','Outdoor','Furniture']
    return render_template("postlist.html", categories=categories)



'''
Return posts data
'''
@app.route('/postlist/<role>', methods=['POST'])
def postListContent(role):
    if not loggedIn():
        if role == 'seller':
            posts = post.searchSellerPosts()
        elif role == 'buyer':
            posts = post.searchBuyerPosts()
        for item in posts:
            item['favorite'] = False
    elif role == 'seller':
        posts = post.searchSellerPosts()
        favorite, _ = account.getFavorite(session['username'])
        for item in posts:
            item['rating'] = post.getRatingOfUser("Seller", item['postId'])
            if str(item['postId']) in favorite:
                item['favorite'] = True
            else:
                item['favorite'] = False
    elif role == 'buyer':
        posts = post.searchBuyerPosts()
        _, favorite = account.getFavorite(session['username'])
        for item in posts:
            item['rating'] = post.getRatingOfUser("Buyer", item['postId'])
            if str(item['postId']) in favorite:
                item['favorite'] = True
            else:
                item['favorite'] = False
    return json.dumps(posts)


'''
Get all the favorite data
'''
@app.route('/favoriteList',methods=['POST'])
def favoriteList():
    userName = session['username']
    sellerFavorite, buyerFavorite = account.getFavorite(userName)
    retList = []

    if sellerFavorite != [""]:
        for f in sellerFavorite:
            tempf = post.searchSellerPosts(postId=int(f))
            if tempf is None:
                break
            tempf['type'] = "Seller"
            retList.append(tempf)

    if buyerFavorite != [""]:
        for f in buyerFavorite:
            tempf = post.searchBuyerPosts(postId=int(f))
            if tempf is None:
                break
            tempf['type'] = "Buyer"
            retList.append(tempf)

    return json.dumps(retList)

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
    if not loggedIn():
        return render_template('login.html', error='Please login first')
    isSeller = flag == "Seller"
    isBuyer = flag == "Buyer"
    postData = post.getPost(postId, flag)
    if isSeller and not postData["valid"]:
        return redirect('/')
    postData["favorite"] = account.searchFavorite(session['username'], postId, flag)
    if postData == None:
        if isSeller:
            return redirect('/NewSellerPost')
        if isBuyer:
            return redirect('/NewBuyerPost')
    return render_template("postdetail.html", seller=isSeller, buyer=isBuyer, post=postData, username=session['username'])


@app.route('/buypostlist',methods=["POST"])
def buypostlist():
    posts = post.searchBuyerPosts(username=session['username'])
    return json.dumps(posts)


@app.route('/sellpostlist',methods=["POST"])
def sellpostlist():
    posts = post.searchSellerPosts(username=session['username'])
    return json.dumps(posts)


'''
Place order page
'''
@app.route('/buyorder', methods=['GET'])
def buyOrder():
    if not loggedIn():
        return render_template('login.html', error='Please login first')
    postId = int(request.args['postId'])
    postData = post.getPost(postId, "Seller")
    if postData == None:
        return render_template('notFound.html'), 404
    return render_template("order.html", item=postData)


'''
Place order
'''
@app.route('/checkout', methods=['POST'])
def checkout():
    if not loggedIn():
        return render_template('login.html', error='Please login first')
    postId = int(request.form['postId'])
    buyerName = session['username']
    transactionType = str(request.form['transactionType'])
    rcvAddress = str(request.form['rcvAddress']) if transactionType == "Online" else None
    orderId = order.createOrder(postId, buyerName, transactionType, rcvAddress)
    if orderId == None:
        return "Placing order failed!"
    message.orderPlaceNotification(postId, orderId)
    return "Placing order succeeded! orderId=" + str(orderId)


'''
Favorite
'''
@app.route('/favorite', methods=['POST'])
def addFavorite():
    if not loggedIn():
        return render_template('login.html', error='Please login first')
    postType = str(request.form['postType'])
    postId = int(request.form['postId'])
    username = session['username']
    if account.addFavorite(username, postId, postType):
        message.userFavoriteNotification(username, postId, postType)
        return "Adding to favorites succeeded!"
    return "Adding to favorites failed!"


'''
Delete favorite
'''
@app.route('/deleteFavorite', methods=['POST'])
def deleteFavorite():
    if not loggedIn():
        return render_template('login.html', error='Please login first')
    postType = str(request.form['postType'])
    postId = int(request.form['postId'])
    username = session['username']
    if account.deleteFavorite(username, postId, postType):
        return "Deleting a favorite item succeeded!"
    return "Deleting a favorite item failed!"


@app.route('/userExist',methods=['POST'])
def userExist():
    username = request.form['username']
    exist = account.searchUser(username = username)
    if exist is not None:
        return 'success'
    else:
        return 'fail'

@app.route('/messageTable',methods=['POST'])
def messageTable():
    #data = [{'username':'kk','time':'1998'},{'username':'bb','time':'2004'},{'username':'ff','time':'123123'}]
    if not loggedIn():
        return render_template('login.html', error='Please login first')
    messages = message.getMessagesByUser(session['username'])
    ret_dict = {}
    for mess in messages:
        another = mess['senderUsername'] if mess['senderUsername'] != session['username'] else mess['receiverUsername']
        if another not in ret_dict:
            ret_dict[another] = {'time':[],'unseen':0}
        ret_dict[another]['time'].append(mess['time'])
        if mess['seen'] == False and mess['receiverUsername'] != another:
            ret_dict[another]['unseen'] += 1
    res = []
    for user,info in ret_dict.items():
        temp_dict = {}
        temp_dict['username'] = user
        temp_dict['time'] = max(info['time'])
        temp_dict['unseen'] = info['unseen']
        res.append(temp_dict)

    res.sort(key=lambda x:x['time'],reverse=True)
    return json.dumps(res)

@app.route('/newMessage',methods=['POST'])
def newMessage():
    if not loggedIn():
        return json.dumps('fail')
    content = str(request.form['content'])
    receiver = str(request.form['receiverUsername'])
    messageId = message.sendMessage(sender=session['username'], receiver=receiver, title='', content=content)
    return json.dumps('success')

@app.route('/getAllMessage',methods=['POST'])
def getAllMessage():
    receiver = request.form['receiver']
    messages = message.getMessages(sender=session['username'], receiver=receiver, currentUser=session['username']) + message.getMessages(sender=receiver, receiver=session['username'], currentUser=session['username'])
    messages = sorted(messages, key=lambda k : k['time'])
    return json.dumps(messages)

@app.route('/getUpdateMessage',methods=['POST'])
def getUpdateMessage():
    receiver = request.form['receiver']
    time = request.form['time']
    messages = []
    s_message = message.getMessages(sender=session['username'], receiver=receiver, currentUser=session['username'])
    r_message = message.getMessages(sender=receiver, receiver=session['username'], currentUser=session['username'])
    if s_message is not None:
        messages += s_message
    if r_message is not None:
        messages += r_message
    messages = sorted(messages, key=lambda k : k['time'])
    messages = list(filter(lambda x:x['time']>time,messages))
    return json.dumps(messages)


'''
Add review on users
'''
@app.route('/addReview', methods=['POST'])
def addReview():
    if not loggedIn():
        return "Please log in first!"
    reviewer = session['username']
    reviewee = str(request.form['reviewee'])
    rating = int(request.form['rating'])
    content = str(request.form['content']) if 'content' in request.form.keys() else None
    orderId = int(request.form['orderId'])
    if not order.checkUser(orderId, session['username']):
        return "No permission"
    reviewId = review.addReview(reviewer, reviewee, rating, content, orderId)
    if reviewId == None:
        return json.dumps("Add Review failed!")
    if order.checkBuyer(orderId, reviewer) and not order.updateStatus(orderId, "Completed"):
        return json.dumps("Update status failed!")
    return json.dumps("Review succeeded!")


'''
Add user info page
'''
@app.route('/UserInfo', methods=['GET'])
def getUserInfo():
    if not loggedIn():
        return render_template('login.html', error='Please login first')
    username = str(request.args['username'])
    rating = account.getRating(username)
    return render_template("user_information.html", username=username, rating=rating)


@app.route('/getReviewsToUser', methods=['POST'])
def getReviewsToUser():
    if not loggedIn():
        return render_template('login.html', error='Please login first')
    reviewee = str(request.form['username'])
    reviewList = review.getReviewToUser(reviewee)
    return json.dumps(reviewList)


'''
Get order for user in current session
'''
@app.route('/orderlist', methods=['POST'])
def getOrderList():
    if not loggedIn():
        return json.dumps('')
    orders = order.getOrderByUser(session['username'])
    return json.dumps(orders)



'''
Get order for given user
'''
@app.route('/transactionlist/<username>', methods=['POST'])
def getTransactionListByUser(username):
    orders = order.getOrderByUser(username)
    orders = filter(lambda item: item["status"]=="Completed", orders)
    return json.dumps(orders)


'''
Order detail page
'''
@app.route('/OrderDetail', methods=['GET'])
def orderDetail():
    if not loggedIn():
        return render_template('login.html', error='Please login first')
    orderId = int(request.args['orderId'])
    if not order.checkUser(orderId, session['username']):
        return redirect("/portal?section=order")
    orderDetail = order.getDetail(orderId)
    if orderDetail is None:
        return redirect('/')
    address = orderDetail.get("receiverAddress")
    if address is not None:
        address = json.loads(address)
    orderDetail["receiverAddress"] = address
    reviewedBySeller = review.checkReviewByOrderAndUser(orderId, orderDetail['sellerName'])
    return render_template("orderdetail.html", order=orderDetail, username=session['username'], reviewedBySeller=reviewedBySeller)


@app.route('/updateOrderStatus', methods=['POST'])
def updateOrderStatus():
    print "update status"
    if not loggedIn():
        return json.dumps('fail')
    orderId = str(request.form['orderId'])
    if not order.checkUser(orderId, session['username']):
        return "No permission"
    status = str(request.form['status'])
    if order.updateStatus(orderId, status):
        print "update succeeded"
        return json.dumps('success')
    print "update failed"
    return json.dumps('fail')


'''
Ship order
'''
@app.route('/shipOrder', methods=['POST'])
def shipOrder():
    if not loggedIn():
        return json.dumps('failed')
    orderId = str(request.form['orderId'])
    if not order.checkUser(orderId, session['username']):
        return "No permission"
    carrier = str(request.form['carrier'])
    trackNo = str(request.form['trackNo'])
    if order.ship(orderId, carrier, trackNo):
        return json.dumps('succeeded')
    return json.dumps('failed')



'''
Cancel order
'''
@app.route('/cancelOrder', methods=['POST'])
def cancelOrder():
    if not loggedIn():
        return json.dumps('Failed!')
    orderId = int(request.form['orderId'])
    if not order.checkUser(orderId, session['username']):
        return "No permission"
    if order.cancelOrder(orderId):
        message.orderCancelNotification(orderId)
        return json.dumps("Succeeded!")
    return json.dumps("Failed!")



'''
Delete post
'''
@app.route('/deletepost', methods=['POST'])
def deletePost():
    if not loggedIn():
        return json.dumps('')
    postType = str(request.form['postType'])
    postId = int(request.form['postId'])
    if post.deletePost(postType, postId):
        return json.dumps("Deleting post succeeded!")
    return json.dumps("Deleting post failed!")


'''
Edit post page
'''
@app.route('/editpost', methods=['GET'])
def editPost():
    if not loggedIn():
        return render_template('login.html', error='Please login first')
    postType = str(request.args['postType'])
    postId = int(request.args['postId'])
    postData = post.getPost(postId, postType)
    role = postType.lower() + "Name"
    if postData[role] != session['username']:
        return render_template('notFound.html'), 404
    postData['postType'] = postType
    return render_template("editpost.html", post=postData)


@app.route('/getPostData', methods=['POST'])
def getPostData():
    if not loggedIn():
        return json.dumps("not logged in")
    postType = str(request.form['postType'])
    postId = int(request.form['postId'])
    postData = post.getPost(postId, postType)
    role = postType.lower() + "Name"
    if postData[role] != session['username']:
        return json.dumps("error")
    postData['postType'] = postType
    return json.dumps(postData)


'''
Edit post action
'''
@app.route('/updatepost', methods=['POST'])
def updatePost():
    if not loggedIn():
        return json.dumps("Please login first")
    postType = str(request.form['postType'])
    postId = int(request.form['postId'])
    updateData = {key : request.form[key] for key in ('title', 'description', 'category', 'price','location') if key in request.form}
    image = request.files.get('image') # None if no such file
    if image == None or image.filename == '':
        image = None
    else:
        image = image.read() # to binary file
        updateData['image'] = image
    if post.updatePost(postType, postId, updateData):
        return json.dumps("Updating post succeeded!")
    return json.dumps("Updating post failed!")

'''
Count unread message for user
'''
@app.route('/countUnreadMessage', methods=['POST'])
def countUnreadMessage():
    if not loggedIn():
        return json.dumps("0")
    messages = message.getMessages(receiver=session['username'], read=False)
    return json.dumps(len(messages))


'''
Comment on posts
'''
@app.route('/addPostComment', methods=['POST'])
def addPostComment():
    if not loggedIn():
        return json.dumps('Please login first')
    postType = str(request.form['postType'])
    postId = str(request.form['postId'])
    author = session['username']
    replyTo = str(request.form['replyTo']) if 'replyTo' in request.form.keys() else None
    content = str(request.form['content'])
    commentId = post_comment.addPostComment(postType, postId, author, replyTo, content)
    if not commentId:
        return json.dumps("add comment failed")
    print postId, postType
    message.newCommentNotification(postId, postType)
    return json.dumps("add comment succeeded, commentId=" + str(commentId))


@app.route('/delPostComment', methods=['POST'])
def delPostComment():
    if not loggedIn():
        return json.dumps('Please login first')
    postType = str(request.form['postType'])
    commentId = str(request.form['commentId'])
    if not post_comment.delPostComment(postType, commentId, session['username']):
        return json.dumps("del comment failed")
    return json.dumps("del comment succeeded")


@app.route('/getPostComments', methods=['POST'])
def getPostComments():
    postType = str(request.form['postType'])
    postId = str(request.form['postId'])
    commentList = post_comment.getPostComments(postType, postId)
    return json.dumps(commentList)


if __name__ == '__main__':
    app.run(debug=True)















