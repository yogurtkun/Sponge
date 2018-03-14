from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

    def __init__(self, username, email, password , zipcode):
        self.username = username
        self.email = email
        self.password = password
        self.zipcode = zipcode

    def __repr__(self):
        return '<User %r>' % self.username


class BuyerPost(db.Model):
    postId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary)
    category = db.Column(db.String(64))
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
    category = db.Column(db.String(64))
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
    user = User(username, email, password, zipcode)
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
        if from_sql(res).get('password') == password:
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