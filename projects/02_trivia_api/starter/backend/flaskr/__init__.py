import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  #allowing origins for any url using the regex r"*"
  CORS(app, resources={r"/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS,PATCH')

    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories")
  def get_categories():
    category=Category.query.all()
    formated_response=[category_item.format() for category_item in category]
    return jsonify({
      'categories':formated_response,
      'total_categories':len(formated_response),
      
      })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/questions")
  def get_paginated_questions():
    question=Question.query.all()
    category=Category.query.all()
    page = request.args.get('page', 1, type=int)
    start= (page - 1)*QUESTIONS_PER_PAGE
    end=start+QUESTIONS_PER_PAGE
    formated_response=[question_item.format() for question_item in question]
    category_formated_response=[category_item.format() for category_item in category]
    return jsonify({
      'questions':formated_response[start:end],
      'total_questions':len(formated_response[start:end]),
      'categories':category_formated_response,
      'current_category':'TBD',
      'page':page
      })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:question_id>",methods=['DELETE'])
  def delete_questions(question_id):
    question=Question.query.get(question_id)
    question.delete()
    return jsonify({"success":True})

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route("/questions",methods=['POST'])
  def new_question():
    response=request.json
    question= response['question']
    answer= response['answer']
    category=response['category']
    difficulty=response['difficulty']
    new_question=Question(question=question, answer=answer, category=category, difficulty=difficulty)
    new_question.insert()
    return jsonify({
      'Success':True,
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route("/questions/search",methods=['POST'])
  def search_questions():
    response=request.json
    term= response['searchTerm']
    print(term)
    questions= Question.query.filter(question.ilike(f'%{term}%')).all()
    formated_response=[question_item.format() for question_item in questions]
    
    return jsonify({
      'questions':formated_response,
      'total_questions':len(formated_response),
      'current_category':"TBD"
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    