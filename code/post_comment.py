from main import schema
from schema import SellerPostComment, BuyerPostComment, from_sql
import datetime

db = schema.db


def addPostComment(postType, postId, author, replyTo, content):
	if postType == "Seller":
		return addSellerPostComment(postId, author, replyTo, content)
	if postType == "Buyer":
		return addBuyerPostComment(postId, author, replyTo, content)


def addSellerPostComment(postId, author, replyTo, content):
	time = datetime.datetime.now()
	comment = SellerPostComment(postId=postId, author=author, replyTo=replyTo, content=content, time=time)
	try:
		db.session.add(comment)
		db.session.commit()
		return comment.commentId
	except Exception as e:
		print e
		db.session.rollback()
		return None


def addBuyerPostComment(postId, author, replyTo, content):
	time = datetime.datetime.now()
	comment = BuyerPostComment(postId=postId, author=author, replyTo=replyTo, content=content, time=time)
	try:
		db.session.add(comment)
		db.session.commit()
		return comment.commentId
	except Exception as e:
		print e
		db.session.rollback()
		return None


def delPostComment(postType, commentId, username):
	if postType == "Seller":
		return delSellerPostComment(commentId, username)
	if postType == "Buyer":
		return delBuyerPostComment(commentId, username)


def delSellerPostComment(commentId, username):
	comment = SellerPostComment.query.get(commentId)
	if comment.author != username:
		return False
	try:
		SellerPostComment.query.filter_by(commentId=commentId).delete()
		db.session.commit()
		return True
	except Exception as e:
		print e
		db.session.rollback()
		return False


def delBuyerPostComment(commentId, username):
	comment = BuyerPostComment.query.get(commentId)
	if comment.author != username:
		return False
	try:
		BuyerPostComment.query.filter_by(commentId=commentId).delete()
		db.session.commit()
		return True
	except Exception as e:
		print e
		db.session.rollback()
		return False



