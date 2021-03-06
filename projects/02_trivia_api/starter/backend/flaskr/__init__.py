import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
   Set up CORS. Allow '*' for origins.
   Delete the sample route after completing the TODOs
  '''
    # allowing origins for any url using the regex r"*"
    CORS(app, resources={r"/*": {"origins": "*"}})
    '''
   Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS,PATCH')

        return response
    '''
  endpoint to handle GET requests
  for all available categories.
  '''
    @app.route("/categories")
    def get_categories():
        try:
            category = Category.query.all()
            formated_response = {
                str(category_item.id): category_item.type
                for category_item in category}
            return jsonify({
                'categories': formated_response,
                'total_categories': len(formated_response)
            })
        except BaseException:
            abort(422)

    '''
  Endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom
   of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route("/questions")
    def get_paginated_questions():
        try:
            questions = [question.format()
                         for question in Question.query.all()]
            questions_count = len(questions)
            category = Category.query.all()
        except BaseException:
            abort(422)
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
        except BaseException:
            abort(405)
        try:
            categories = {
                str(category_item.id): category_item.type
                for category_item in category}
            if questions[start:end]:
                return jsonify({
                    'questions': questions[start:end],
                    'totalQuestions': questions_count,
                    'categories': categories,
                    'page': page
                })
            else:
                abort(404)
        except Exception as e:
            abort(404)
    '''
  Endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question,
  the question will be removed.
  This removal will persist in the database
  and when you refresh the page.
  '''
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_questions(question_id):
        question = Question.query.get(question_id)
        if question:
            question.delete()
            return jsonify({"delete_id": question_id})
        else:
            abort(404)

    '''
  Endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route("/questions", methods=['POST'])
    def new_question():
        response = {}
        try:
            response = request.json
            question = response['question']
            answer = response['answer']
            category = response['category']
            difficulty = response['difficulty']
        except BaseException:
            abort(405)

        try:
            new_question = Question(
                question=question, answer=answer,
                category=category, difficulty=difficulty)
            new_question.insert()
            return jsonify(request.json)
        except Exception as e:
            abort(422)

    '''
  Endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route("/questions/search", methods=['POST'])
    def search_questions():
        try:
            response = request.json
            term = response['searchTerm']
        except BaseException:
            abort(405)
        questions = None
        # Catch if the query failed unexpectedly
        try:
            questions = Question.query.filter(
                Question.question.ilike(f'%{term}%')).all()
        except BaseException:
            abort(422)
        formated_response = [question_item.format()
                             for question_item in questions]
        if len(formated_response):
            return jsonify({
                'questions': formated_response,
                'total_questions': len(formated_response)
            })
        else:
            abort(404)

    '''
  @Endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

    @app.route("/categories/<int:category_id>/questions")
    def questions_by_category(category_id):
        try:
            if(category_id != 0):
                current_category = Category.query.get(category_id)
                questions = Question.query.filter_by(
                    category=str(category_id)).all()
                resp_current_category_type = current_category.type
            else:
                # Creating the possiblity to invoke all questions by passing 0
                # in category_id parameter
                current_category = 0
                questions = Question.query.all()
                resp_current_category_type = "ALL"

            questions = [question.format() for question in questions]
            return jsonify({
                "questions": questions,
                "totalQuestions": len(questions),
                "currentCategory": resp_current_category_type})
        except BaseException:
            # Category is not found
            abort(404)

    '''
   POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def quizes():
        try:
            quiz_category = request.json['quiz_category']['id']
            # quiz_category: Has TO BE AN INTEGER REFERING TO CATEGORY ID
            quiz_category = int(quiz_category)
            previous_questions = request.json['previous_questions']
        except BaseException:
            # if json payload is invalid
            abort(405)
        if quiz_category != 0:
            questions = [question.format() for question in db.session.query(
                Question)
                .filter_by(category=quiz_category)
                .order_by(func.random()).all()]
        else:
            questions = [question.format() for question in db.session.query(
                Question).order_by(func.random()).all()]

        # TODO: REVISE: I am not sure how to use
        # Question.id.in_(previous_questions)
        questions = [q for q in questions if q['id']
                     not in previous_questions]

        if len(questions):
            # Never stop questioning until all questions are passed by
            return jsonify({
                'question': questions[0]
            })
        # GAME OVER!
        return jsonify({
        })

    '''
  Error handlers for all expected errors
  including 404 and 422.
  '''
    # handling 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": 404,
            "message": "Resource Not Found On Server "
        }), 404
    # handling 405

    @app.errorhandler(405)
    def Invalid_req(error):
        return jsonify({
            "error": 405,
            "message": "Invalid Request Payload Or Structure"
        }), 405
    # handling 422

    @app.errorhandler(422)
    def unprocessable_res_err(error):
        return jsonify({
            "error": 422,
            "message": "Resource Cannot Be Processed"
        }), 422
    # handling 500

    def server_err(error):
        return jsonify({
            "error": 500,
            "message": "Opps, Something Went Wrong.\
            Please Contact Adminstrator "
        }), 500

    return app
