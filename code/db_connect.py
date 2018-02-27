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
    print(data)
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

def newUser(username,email,password,zipcode):
    newuser = User(username,email,password,zipcode)
    db.session.add(newuser)
    db.session.commit()

    return from_sql(newuser)


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
        newUser("1","1","1","1")
    print("All tables created")


if __name__ == '__main__':
    _create_database()