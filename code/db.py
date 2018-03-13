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

    def __init__(self, username, email, password , zipcode):
        self.username = username
        self.email = email
        self.password = password
        self.zipcode = zipcode

    def __repr__(self):
        return '<User %r>' % self.username


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
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()