import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_udacity"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Variables To Help in Tests
        self.new_question = {
            "question": "How many players in a football team?",
            "answer": "11 Players in every team",
            "difficulty": 2,
            "category": 4
        }
        self.bad_question = {

        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        self.db.get_engine(self.app).dispose()  # This

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['total_categories'], 6)

    def test_invalid_request_getting_category(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    def test_get_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)

    # Exception going for a page that has no questions results in 404

    def test_no_paginate_questions(self):
        res = self.client().get('/questions?page=9999999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_sucsse_delete_question(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['delete_id'])

    def test_failed_deleting_question(self):
        res = self.client().delete('/questions/400')
        self.assertEqual(res.status_code, 404)

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['question'])

   
    def test_mailformed_create_question(self):
        res = self.client().post('/questions', json=self.bad_question)
        self.assertEqual(res.status_code, 405)

    def test_search_questions(self):
        data = {
            'searchTerm': 's'
        }
        res = self.client().post('/questions/search', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])

    def test_bad_search_questions(self):
        data = {
            'searchTerm': 'الqwqwشس29@'
        }
        res = self.client().post('/questions/search', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_question_search_with_category(self):

        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['currentCategory'], 'Art')
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['questions'])

    def test_question_search_with_non_existent_category(self):

        res = self.client().get('/categories/9/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_get_quizzes(self):

        data = {
            "previous_questions": [1, 2, 3, 4],
            "quiz_category": {"type": "click", "id": 0}
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['question'])
        self.assertNotEqual(data['question']['id'], 1)
        self.assertNotEqual(data['question']['id'], 2)

    def test_mailformed_quiz_request_format(self):
        data = {
            "previous_questions": [],
            "quiz_category": {"type": "click", "id": "Your Request\
                Is a Failure"}
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    # Testing Being in the middle of a quiz

    def test_play_quizes(self):

        data = {
            "previous_questions": [1, 2, 3, 4],
            "quiz_category": {"type": "click", "id": 0}
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['question'])
        self.assertNotEqual(data['question']['id'], 4)
        self.assertNotEqual(data['question']['id'], 1)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
