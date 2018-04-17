from main import schema
from schema import Message, Order, from_sql, db
import account, post
import datetime
import pytz
from sqlalchemy import or_
    

def sendMessage(receiver, content, sender='system', title=''):
    # create system account if not exists
    if sender == 'system' and account.searchUser('system') is None:
        account.registerUser('system', 'system@domain.com', 'system-pwd', 10000)

    time = datetime.datetime.now(pytz.timezone('US/Eastern'))
    message = Message(senderUsername=sender, receiverUsername=receiver, title=title, content=content, time=time)
    try:
        db.session.add(message)
        db.session.commit()
        return message.messageId
    except Exception as e:
        print e
        db.session.rollback()
        return None



def getMessages(currentUser=None, sender=None, receiver=None, read=None):
    try:
        query = Message.query
        if sender is not None:
            query = query.filter_by(senderUsername=sender)
        if receiver is not None:
            query = query.filter_by(receiverUsername=receiver)
        if read is not None:
            query = query.filter_by(seen=read)
        messages = []
        for message in query.all():
            messages.append(from_sql(message))
        query.filter_by(receiverUsername=currentUser).update(dict(seen=True))
        db.session.commit()
        return messages
    except Exception as e:
        print e
        db.session.rollback()
        return None



'''
Get message of which the receiver or sender is the given user
'''
def getMessagesByUser(username):
    try:
        query = Message.query.filter(or_(Message.senderUsername == username, Message.receiverUsername == username))
        messages = []
        for message in query.all():
            messages.append(from_sql(message))
        return messages
    except Exception as e:
        print e
        return None



def orderStatusNotification(orderId, status):
    order = Order.query.get(orderId)
    msg = "Status of order " + str(orderId) + " has changed to " + status + "."
    sendMessage(sender="system", receiver=order.buyerName, content=msg)
    sendMessage(sender="system", receiver=order.sellerName, content=msg)



def userFavoriteNotification(username, postId, postType):
    if postType == "Seller":
        postItem = post.getPost(postId, postType)
        poster = postItem['sellerName']
        title = postItem['title']
    if postType == 'Buyer':
        postItem = post.getPost(postId, postType)
        poster = postItem['buyerName']
        title = postItem['title']
    msg = username + " has added your post " + title + " with Id " + str(postId) + " to favorite list."
    sendMessage(sender="system", receiver=poster, content=msg)


def orderPlaceNotification(postId, orderId):
    order = Order.query.get(orderId)
    sellerName = order.sellerName
    buyerName = order.buyerName
    msg = buyerName + " has placed on order(" + str(orderId) + ") on your post(" + str(postId) + ")."
    sendMessage(sender="system", receiver=sellerName, content=msg)
    msg = "You have placed an order(" + str(orderId) + ") on post(" + str(postId) + ")."
    sendMessage(sender="system", receiver=buyerName, content=msg)


def orderCancelNotification(orderId):
    msg = "Order " + str(orderId) + " is canceled."
    order = Order.query.get(orderId)
    sendMessage(sender="system", receiver=order.buyerName, content=msg)
    sendMessage(sender="system", receiver=order.sellerName, content=msg)


def newCommentNotification(postId, postType):
    if postType == "Seller":
        postItem = post.getPost(postId, postType)
        poster = postItem['sellerName']
        title = postItem['title']
    if postType == 'Buyer':
        postItem = post.getPost(postId, postType)
        poster = postItem['buyerName']
        title = postItem['title']
    msg = "Your " + postType + " post " + title + " with Id " + str(postId) + " has a new comment."
    sendMessage(sender="system", receiver=poster, content=msg)


