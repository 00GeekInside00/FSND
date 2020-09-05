import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# database_name = "trivia_udacity"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)

# database_path="postgres://wtufwwks:JM9TJYtSDFIdBXi7Y9XYl78PRD7dPK5a@kandula.db.elephantsql.com:5432/wtufwwks"
# database_path = "postgres://nrsdyucjnfhenp:4c17438a512b2a307923e5464f2ec1ad4c677d8e3cc77a26d826673e0a677170@ec2-54-217-213-79.eu-west-1.compute.amazonaws.com:5432/d9ll3obff1cu1u" 
database_path = "postgres://nrsdyucjnfhenp:4c17438a512b2a307923e5464f2ec1ad4c677d8e3cc77a26d826673e0a677170@ec2-54-217-213-79.eu-west-1.compute.amazonaws.com:5432/d9ll3obff1cu1u" 

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True, autoincrement=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True, autoincrement=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }