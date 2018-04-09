from main import schema
from schema import Order, from_sql
from post import searchSellerPosts, getPost, invalidSellerPost, validSellerPost
import account
import datetime

db = schema.db

def createOrder(postId, buyerName, transactionType, rcvAddress):
    time = datetime.datetime.now()
    post = searchSellerPosts(postId)
    if post == None:
        return None
    if not invalidSellerPost(postId):
        return None
    sellerName = post['sellerName']
    seller = account.searchUser(sellerName)
    if seller == None:
        return None
    sndAddress = seller['address']
    order = Order(postId=postId, buyerName=buyerName, sellerName=sellerName, time=time, status="In progress", transactionType=transactionType, senderAddress=sndAddress, receiverAddress=rcvAddress)
    try:
        db.session.add(order)
        db.session.commit()
        return order.orderId
    except Exception as e:
        print e
        db.session.rollback()
        return None


def cancelOrder(orderId):
    try:
        order = from_sql(Order.query.get(orderId))
        postId = order['postId']
        if not validSellerPost(postId):
            return False
        Order.query.filter_by(orderId=orderId).delete()
        db.session.commit()
        return True
    except Exception as e:
        print e
        db.session.rollback()
        return False


def getDetail(orderId):
    if Order.query.get(orderId) is None:
        return None
    order = from_sql(Order.query.get(orderId))
    postId = order['postId']
    post = searchSellerPosts(postId)
    orderDetail = {}
    for d in [post, order]:
        orderDetail.update(d)
    return orderDetail


def checkOrderByPost(postId):
    try:
        count = Order.query.filter_by(postId=postId).count()
        if count == 0:
            return False
        else:
            return True
    except:
        return False


def getOrderByUser(username):
    orders = []
    for order in Order.query.filter_by(sellerName=username).all():
        order = from_sql(order)
        order['type'] = 'selling'
        orders.append(order)
    for order in Order.query.filter_by(buyerName=username).all():
        order = from_sql(order)
        order['type'] = 'buying'
        orders.append(order)
    for order in orders:
        post = getPost(order['postId'], 'Seller')
        order['product'] = post['title']
        order['price'] = post['price']
    return orders


def updateStatus(orderId, status):
    states = ['In progress', 'Confirmed', 'Shipped', 'Completed']
    order = Order.query.get(orderId)
    if order.transactionType != 'Online':
        states.remove('Shipped')
    if states.index(order.status) + 1 == states.index(status):
        order.status = status.transa
    else:
        return False
    try:
        db.session.commit()
        return True
    except Exception as e:
        print e
        db.session.rollback()
        return False


def ship(orderId, carrier, trackNo):
    order = Order.query.get(orderId)
    try:
        order.carrier = carrier
        order.trackNo = trackNo
        db.session.commit()
        return True
    except Exception as e:
        print e
        db.session.rollback()
        return False








