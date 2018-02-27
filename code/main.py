from google.appengine.ext import vendor
vendor.add('lib')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)

# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='dummy_region',
#     aws_access_key_id='dummy_access_key',
#     aws_secret_access_key='dummy_secret_key',
#     verify=False)

def connect_db():
    with app.app_context():
        db = SQLAlchemy()
        app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        db.init_app(app)
        result = db.session.execute("SELECT * From test").fetchone()
        db.session.close()
        return str(result)

@app.route('/')
def index():
    return "Hello, World (lets see how long a change takes III)!"

if __name__ == '__main__':
    app.run(debug=True)
