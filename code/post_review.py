from main import schema
from schema import SellerPostReview, BuyerPostReview, from_sql
import datetime

db = schema.db


def addPostReview(postType, postId, author, title, content):
	if postType == "Seller":
		return addSellerPostReview(postId, author, title, content)
	if postType == "Buyer":
		return addBuyerPostReview(postId, author, title, content)


def addSellerPostReview(postId, author, title, content):
	time = datetime.datetime.now()
	review = SellerPostReview(postId=postId, author=author, title=title, content=content, time=time)
	try:
		db.session.add(review)
		db.session.commit()
		return review.reviewId
	except Exception as e:
		print e
		db.session.rollback()
		return None


def addBuyerPostReview(postId, author, title, content):
	time = datetime.datetime.now()
	review = BuyerPostReview(postId=postId, author=author, title=title, content=content, time=time)
	try:
		db.session.add(review)
		db.session.commit()
		return review.reviewId
	except Exception as e:
		print e
		db.session.rollback()
		return None


def delPostReview(postType, reviewId, username):
	if postType == "Seller":
		return delSellerPostReview(reviewId, username)
	if postType == "Buyer":
		return delBuyerPostReview(reviewId, username)


def delSellerPostReview(reviewId, username):
	review = SellerPostReview.query.get(reviewId)
	if review.author != username:
		return False
	try:
		SellerPostReview.query.filter_by(reviewId=reviewId).delete()
		db.session.commit()
		return True
	except Exception as e:
		print e
		db.session.rollback()
		return None


def delBuyerPostReview(reviewId, username):
	review = BuyerPostReview.query.get(reviewId)
	if review.author != username:
		return False
	try:
		BuyerPostReview.query.filter_by(reviewId=reviewId).delete()
		db.session.commit()
		return True
	except Exception as e:
		print e
		db.session.rollback()
		return None