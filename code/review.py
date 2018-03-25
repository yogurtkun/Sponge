from main import schema
from schema import Review, from_sql
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
