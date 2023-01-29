import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service.
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
User
Represents as User of the website. Able to create listings.
'''
class User(db.Model):  
  __tablename__ = 'User'

  id = Column(db.Integer, primary_key=True)
  username = Column(String(80))
  email = Column(String(500))
  listings = db.relationship('Listing', backref='user')

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'username': self.username,
      'email': self.email
      }


'''
Listing
Represents a listing which will contain title, subtitle, description, image, text body and publish dates
'''
class Listing(db.Model):
  __tablename__ = 'Listing'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(180))
  subtitle = db.Column(db.String(180))
  description = db.Column(db.String(500))
  image = db.Column(db.String)
  body = db.Column(db.String)
  publish_dates = db.Column(db.ARRAY(db.String(120)))

  def __init__(self, title="", subtitle="", description="", image="", body="", publish_dates=[]):
    self.title = title
    self.subtitle = subtitle
    self.description = description
    self.image = image
    self.body = body
    self.publish_dates = publish_dates

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'subtitle': self.subtitle,
      'description': self.description,
      'image': self.image,
      'body': self.body,
      'publish_dates': self.publish_dates
      }