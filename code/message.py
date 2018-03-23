from main import schema
from schema import Message, from_sql, db
import account
import datetime
from sqlalchemy import or_
	

def sendMessage(receiver, title, content, sender='system'):
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



def getMessages(sender=None, receiver=None):
	try:
		query = Message.query
		if sender is not None:
			query.filter_by(senderUsername=sender)
		if receiver is not None:
			query.filter_by(receiverUsername=receiver)
		messages = []
		for message in query.all():
			messages.append(from_sql(message))
		return messages
	except Exception as e:
		print e
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
