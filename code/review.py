from main import schema
from schema import Review, Order, SellerPost, from_sql
import account
import datetime

db = schema.db

def addReview(reviewer, reviewee, rating, content, orderId):
	time = datetime.datetime.now()
	review = Review(reviewer=reviewer, reviewee=reviewee, rating=rating, content=content, orderId=orderId, time=time)
	try:
		db.session.add(review)
		db.session.commit()
		if not account.updateRating(reviewee, rating):
			return None
		return from_sql(review)
	except Exception as e:
		print e
		db.session.rollback()
		return None


def getReviewToUser(reviewee):
	res = Review.query.filter_by(reviewee=reviewee).all()
	reviews = []
	for r in res:
		reviews.append(from_sql(r))
	for r in reviews:
		orderId = r['orderId']
		order = Order.query.get(orderId)
		postId = order.postId
		post = SellerPost.query.get(postId)
		orderTitle = post.title
		r['orderTitle'] = orderTitle
	return reviews