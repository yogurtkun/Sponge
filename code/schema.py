from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import base64
import os
import datetime

db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data.pop('_sa_instance_state')

    if 'time' in data:
        data['time'] = str(data['time'])
    if 'image' in data and data['image'] is not None:
        image = data['image']
        data['image'] = base64.b64encode(image).decode('ascii')
    return data    


class User(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(32), unique = True)
    password = db.Column(db.String(16),  nullable=False)
    zipcode = db.Column(db.String(16))
    phoneNumber = db.Column(db.String(16))
    address = db.Column(db.Text)
    rating = db.Column(db.Float) # average rating
    ratingCount = db.Column(db.Integer) # number of rating
    sellerPosts = db.Column(db.String(128), server_default='') # seller post list
    buyerPosts = db.Column(db.String(128), server_default='') # buyer post list
    favoriteSellerPosts = db.Column(db.String(128), server_default='')
    favoriteBuyerPosts = db.Column(db.String(128), server_default='')

    def __repr__(self):
        return '<User %r>' % self.username


class BuyerPost(db.Model):
    postId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary)
    category = db.Column(db.Enum('Beauty','Books','Electronics','Clothing','Accessories','Health','Kitchen','Music','Software','Outdoor','Furniture'))
    price = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    location = db.Column(db.String(32))
    buyerName = db.Column(db.String(32), db.ForeignKey('user.username', ondelete='CASCADE'))
    user = db.relationship("User", lazy=True, cascade="all,delete")

    def __repr__(self):
        return '<BuyerPost %r>' % self.postId


class SellerPost(db.Model):
    postId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary)
    category = db.Column(db.Enum('Beauty','Books','Electronics','Clothing','Accessories','Health','Kitchen','Music','Software','Outdoor','Furniture'))
    price = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    location = db.Column(db.String(32))
    sellerName = db.Column(db.String(32), db.ForeignKey('user.username', ondelete='CASCADE'))
    user = db.relationship("User", lazy=True, cascade="all,delete")
    valid = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<SellPost %r>' % self.postId


class SellerPostReview(db.Model):
    reviewId = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('seller_post.postId', ondelete='CASCADE'))
    sellerPost = db.relationship("SellerPost", lazy=True)
    author = db.Column(db.String(32), db.ForeignKey('user.username', ondelete='CASCADE'))
    user = db.relationship("User", lazy=True, cascade="all,delete")
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Review %r>' % self.reviewId


class BuyerPostReview(db.Model):
    reviewId = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('buyer_post.postId', ondelete='CASCADE'))
    buyerPost = db.relationship("BuyerPost", lazy=True)
    author = db.Column(db.String(32), db.ForeignKey('user.username', ondelete='CASCADE'))
    user = db.relationship("User", lazy=True, cascade="all,delete")
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Review %r>' % self.reviewId


class Order(db.Model):
    orderId = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('seller_post.postId', ondelete='CASCADE'))
    sellerPost = db.relationship("SellerPost", lazy=True)
    buyerName = db.Column(db.String(32), db.ForeignKey("user.username", ondelete='CASCADE'))
    buyer = db.relationship("User", foreign_keys=[buyerName], lazy=True, cascade="all,delete")
    sellerName = db.Column(db.String(32), db.ForeignKey("user.username", ondelete='CASCADE'))
    seller = db.relationship("User", foreign_keys=[sellerName], lazy=True, cascade="all,delete")
    time = db.Column(db.DateTime)
    status = db.Column(db.Enum("In progress", "Confirmed", "Shipped", "Completed"))
    transactionType = db.Column(db.String(32))
    senderAddress = db.Column(db.Text)
    receiverAddress = db.Column(db.Text)
    carrier = db.Column(db.Enum("USPS", "FedEx", "UPS", "DHL"))
    trackNo = db.Column(db.String(64))

    def __repr__(self):
        return '<Order %r>' % self.orderId


class Message(db.Model):
    messageId = db.Column(db.Integer, primary_key=True)
    senderUsername = db.Column(db.String(32), db.ForeignKey("user.username", ondelete='CASCADE'))
    sender = db.relationship("User", foreign_keys=[senderUsername], lazy=True, cascade="all,delete")
    receiverUsername = db.Column(db.String(32), db.ForeignKey("user.username", ondelete='CASCADE'))
    receiver = db.relationship("User", foreign_keys=[receiverUsername], lazy=True, cascade="all,delete")
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime)
    seen = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Message %r>' % messageId


class Review(db.Model):
    reviewId = db.Column(db.Integer, primary_key=True)
    # who write the review
    reviewer = db.Column(db.String(32), db.ForeignKey("user.username", ondelete='CASCADE'))  
    reviewerUser = db.relationship("User", foreign_keys=[reviewer], lazy=True, cascade="all,delete")
    # who receives the review
    reviewee = db.Column(db.String(32), db.ForeignKey("user.username", ondelete='CASCADE'))
    revieweeUser = db.relationship("User", foreign_keys=[reviewee], lazy=True, cascade="all,delete")
    rating = db.Column(db.Integer)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    # a review must be related to an order
    orderId = db.Column(db.Integer, db.ForeignKey("order.orderId", ondelete='CASCADE'), nullable=False)
    order = db.relationship("Order", foreign_keys=[orderId], lazy=True, cascade="all,delete")

    def __repr__(self):
        return '<Review %r>' % reviewId

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('./config.py')
    init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
    print("All tables created")  

if __name__ == '__main__':
    _create_database()
