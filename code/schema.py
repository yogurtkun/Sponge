from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import base64

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
    sellerPosts = db.Column(db.String(128)) # seller post list
    buyerPosts = db.Column(db.String(128)) # buyer post list
    favoriteSellerPosts = db.Column(db.String(128))
    favoriteBuyerPosts = db.Column(db.String(128))

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
    buyerName = db.Column(db.String(32), db.ForeignKey('user.username'))
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
    sellerName = db.Column(db.String(32), db.ForeignKey('user.username'))
    user = db.relationship("User", lazy=True, cascade="all,delete")

    def __repr__(self):
        return '<SellPost %r>' % self.postId


class Order(db.Model):
    orderId = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('seller_post.postId'))
    sellerPost = db.relationship("SellerPost", lazy=True)
    buyerName = db.Column(db.String(32), db.ForeignKey("user.username"))
    buyer = db.relationship("User", foreign_keys=[buyerName], lazy=True, cascade="all,delete")
    sellerName = db.Column(db.String(32), db.ForeignKey("user.username"))
    seller = db.relationship("User", foreign_keys=[sellerName], lazy=True, cascade="all,delete")
    time = db.Column(db.DateTime)
    status = db.Column(db.String(32))
    transactionType = db.Column(db.String(32))
    senderAddress = db.Column(db.Text)
    receiverAddress = db.Column(db.Text)

    def __repr__(self):
        return '<Order %r>' % self.orderId


class Message(db.Model):
    messageId = db.Column(db.Integer, primary_key=True)
    senderUsername = db.Column(db.String(32), db.ForeignKey("user.username"))
    sender = db.relationship("User", foreign_keys=[senderUsername], lazy=True, cascade="all,delete")
    receiverUsername = db.Column(db.String(32), db.ForeignKey("user.username"))
    receiver = db.relationship("User", foreign_keys=[receiverUsername], lazy=True, cascade="all,delete")
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Message %r>' % messageId



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
