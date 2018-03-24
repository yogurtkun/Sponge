from main import schema
from schema import Review
import datetime

db = schema.db

def addReview(reviewerUsername, revieweeUsername, rating, content, orderId):
	userReview = UserReview(reviewerUsername=reviewerUsername, revieweeUsername=revieweeUsername, rating=rating, content=content, orderId=orderId)
