from main import schema
from schema import Order, from_sql
from post import searchSellerPosts
import account
import datetime

db = schema.db

def createOrder(postId, buyerName, transactionType, rcvAddress):
	time = datetime.datetime.now()
	post = searchSellerPosts(postId)
	if post == None:
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