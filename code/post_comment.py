from main import schema
from schema import SellerPostComment, BuyerPostComment, from_sql
import datetime

db = schema.db


def addPostComment(postType, postId, author, title, content):
	if postType == "Seller":
		return addSellerPostComment(postId, author, title, content)
	if postType == "Buyer":
		return addBuyerPostComment(postId, author, title, content)


def addSellerPostComment(postId, author, title, content):
	time = datetime.datetime.now()
	review = SellerPostComment(postId=postId, author=author, title=title, content=content, time=time)
	try:
		db.session.add(review)
		db.session.commit()
		return review.reviewId
	except Exception as e:
		print e
		db.session.rollback()
		return None


def addBuyerPostComment(postId, author, title, content):
	time = datetime.datetime.now()
	review = BuyerPostComment(postId=postId, author=author, title=title, content=content, time=time)
	try:
		db.session.add(review)
		db.session.commit()
		return review.reviewId
	except Exception as e:
		print e
		db.session.rollback()
		return None


def delPostComment(postType, reviewId, username):
	if postType == "Seller":
		return delSellerPostComment(reviewId, username)
	if postType == "Buyer":
		return delBuyerPostComment(reviewId, username)


def delSellerPostComment(reviewId, username):
	review = SellerPostComment.query.get(reviewId)
	if review.author != username:
		return False
	try:
		SellerPostComment.query.filter_by(reviewId=reviewId).delete()
		db.session.commit()
		return True
	except Exception as e:
		print e
		db.session.rollback()
		return None


def delBuyerPostComment(reviewId, username):
	review = BuyerPostComment.query.get(reviewId)
	if review.author != username:
		return False
	try:
		BuyerPostComment.query.filter_by(reviewId=reviewId).delete()
		db.session.commit()
		return True
	except Exception as e:
		print e
		db.session.rollback()
		return None