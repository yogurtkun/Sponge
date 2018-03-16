from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import enum
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
    return data    

class Category(enum.Enum):
    Beauty = 'Beauty'
    Books = 'Books'
    Electronics = 'Electronics'
    Clothing = 'Clothing'
    Accessories = 'Accessories'
    Health = 'Health'
    Kitchen = 'Kitchen'
    Music = 'Music'
    Software = 'Software'
    Outdoor = 'Outdoor'
    Furniture = 'Furniture'

class User(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(32), unique = True)
    password = db.Column(db.String(16),  nullable=False)
    zipcode = db.Column(db.String(16))
    phoneNumber = db.Column(db.String(16))
    address = db.Column(db.Text)
    rating = db.Column(db.Integer)
    wantToSell = db.Column(db.String(128))
    wantToBuy = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    def checkPassword(self, pw):
        if pw == self.password:
            return True
        return False


class BuyerPost(db.Model):
    postId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary)
    category = db.Column(db.Enum(Category))
    price = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    location = db.Column(db.String(32))
    buyerName = db.Column(db.String(32), db.ForeignKey('user.username'))
    user = db.relationship("User", lazy=True)

    def __repr__(self):
        return '<BuyerPost %r>' % self.postId


class SellerPost(db.Model):
    postId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary)
    category = db.Column(db.Enum(Category))
    price = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    location = db.Column(db.String(32))
    sellerName = db.Column(db.String(32), db.ForeignKey('user.username'))
    user = db.relationship("User", lazy=True)

    def __repr__(self):
        return '<SellPost %r>' % self.postId


class Order(db.Model):
    orderId = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('seller_post.postId'))
    sellerPost = db.relationship("SellerPost", lazy=True)
    buyerName = db.Column(db.String(32), db.ForeignKey("user.username"))
    buyer = db.relationship("User", foreign_keys=[buyerName], lazy=True)
    sellerName = db.Column(db.String(32), db.ForeignKey("user.username"))
    seller = db.relationship("User", foreign_keys=[sellerName], lazy=True)
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
    sender = db.relationship("User", foreign_keys=[senderUsername], lazy=True)
    receiverUsername = db.Column(db.String(32), db.ForeignKey("user.username"))
    receiver = db.relationship("User", foreign_keys=[receiverUsername], lazy=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Message %r>' % messageId


def registerUser(username, email, password, zipcode):
    user = User(username=username, email=email, password=password, zipcode=zipcode)
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def loginUser(username, password):
    res = User.query.get(username)
    if res:
        if res.checkPassword(password):
            return 1
        return -1 # wrong password
    return 0 # user doesn't exist


def searchUser(username):
    res = User.query.get(username)
    if res:
        return from_sql(res)
    return None


def deleteUser(username):
    try:
        User.query.filter_by(username=username).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def deleteSellerPostById(postId):
    try:
        SellerPost.query.filter_by(postId = postId).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def deleteSellerPostByUser(username):
    try:
        SellerPost.query.filter_by(sellerName = username).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def createSellerPost(title, description, category, price, location, image, sellerName):
    time = datetime.datetime.now()
    post = SellerPost(title=title, description=description, category=category, price=price, location=location, image=image, sellerName=sellerName, time=time)
    try:
        db.session.add(post)
        db.session.commit()
        return post.postId
    except:
        db.session.rollback()
        return None


def searchSellerPosts(postId=None):
    try:
        if postId is None:
            #   return all the sell posts
            #   not support paging
            posts = []
            for post in SellerPost.query.all():
                posts.append(from_sql(post))
            return posts
        else:
            post = SellerPost.query.get(postId)
            return from_sql(post)
    except:
        return None


def searchBuyerPosts(postId=None):
    try:
        if postId is None:
            #   return all the sell posts
            #   not support paging
            posts = []
            for post in BuyerPost.query.all():
                posts.append(from_sql(post))
            return posts
        else:
            post = BuyerPost.query.get(postId)
            return from_sql(post)
    except:
        return None


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
