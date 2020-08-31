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
        self.database_name = "trivia_udacity_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Variables To Help in Tests
        self.empty_question = {
            'question': '',
            'answer': '',
            'category': 1,
            'difficulty': 1
        }
        self.new_question = {
            'question': 'How many Pyramids Are There In Egypt?',
            'answer': '108',
            'category': 3,
            'difficulty': 3
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def get_categories(self):
        res = self.client().get('/categories')                 
        data = json.loads(res.data)                            

        self.assertEqual(res.status_code, 200)                       
        self.assertTrue(data['categories'])                    
        self.assertEqual(len(data['categories']), 6)           
        


  
    def get_paginate_questions(self):
        
        res = self.client().get('/questions')                    
        data = json.loads(res.data)                              
        
        self.assertEqual(res.status_code, 200)                   
        self.assertTrue(data['categories'])
        self.assertTrue(data['totalQuestions'])                 
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)            


   
    def no_paginate_questions(self):
        res = self.client().get('/questions?page=9999999')     
        data = json.loads(res.data)                              
        self.assertEqual(res.status_code, 404)                  


    
    def test_sucsse_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)               

        self.assertEqual(res.status_code, 200)    
        self.assertTrue(data['delete_id'])

    def create_question(self):
        res = self.client().post('/questions', json=self.new_question)  .assertEqual(res.status_code, 200)                          
        self.assertIsNotNone(data['question'])


    def search_questions(self):        
        data={
            'searchTerm': 'ment'
        }
        res = self.client().post('/questions/search', json=data)   
        data = json.loads(res.data)                                      
        self.assertEqual(res.status_code, 200)                          
        self.assertIsNotNone(data['questions'])

       

    def question_search_with_category(self):
        
        res = self.client().get('/categories/2/questions') 
        data = json.loads(res.data)                                     

        self.assertEqual(res.status_code, 200)                           
        self.assertEqual(data['categories'], 'Art')
        self.assertTrue(data['categories'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['questions'])


    def get_quizzes(self):
        
        data={
            	"previous_questions": [1,2,3,4],
	            "quiz_category": {"type": "click", "id": 0}
        }
        res = self.client().post('/quizzes', json=data)    
        data = json.loads(res.data)                              
        self.assertEqual(res.status_code, 200)                  
        self.assertIsNotNone(data['question'])
        self.assertNotEqual(data['question']['id'], 1)
        self.assertNotEqual(data['question']['id'], 2)


    def play_quizes(self):

        data={
            	"previous_questions": [1,2,3,4],
	            "quiz_category": {"type": "Art", "id": 2}
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