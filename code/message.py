from main import schema
from schema import Message, Order, from_sql, db
import account, post
import datetime
from sqlalchemy import or_
    

def sendMessage(receiver, content, sender='system', title=''):
    # create system account if not exists
    if sender == 'system' and account.searchUser('system') is None:
        account.registerUser('system', 'system@domain.com', 'system-pwd', 10000)

    time = datetime.datetime.now()
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
            if message.receiver == currentUser:
                message.seen = True
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
    msg = "Status of order " + str(orderId) + " has changed to " + status
    sendMessage(sender="system", receiver=order.buyerName, content=msg)
    sendMessage(sender="system", receiver=order.sellerName, content=msg)



def userFavoriteNotification(username, postId, postType):
    if postType == "Seller":
        poster = post.getPost(postId, postType)['sellerName']
    if postType == 'Buyer':
        poster = post.getPost(postId, postType)['buyerName']
    msg = username + "has add your post with Id " + str(postId) + " to favorite list"
    sendMessage(sender="system", receiver=poster, content=msg)




