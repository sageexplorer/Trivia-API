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
        self.database_name = "test_trivia"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    def test_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200, 'Response status is not 200')

    def test_questions_with_not_existing_pagination(self):
        res = self.client().get('/questions/?page=900')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404, 'Response status is not 404')
  

    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200, 'Response status is not 200')
 

    def test_create_new_questions(self):
        data = {
            'question': 'What is the highest mountain in the world?',
            'answer': 'Mt. Everest',
            'category': 3,
            'difficulty': 1
        }
        res = self.client().post('/questions', json = data)
        self.assertEqual(res.status_code, 200, 'POST is not succesful!')
    
    def test_delete_the_last_post(self):
        '''get the id of the last post'''
        body = {'searchTerm': 'highest mountain'}
        res = self.client().post('/search', json=body)
        data = json.loads(res.data)
        id = int(data['questions'][-1]['id'])
        del_res = self.client().delete(f'/questions/{id}')
        self.assertEqual(del_res.status_code, 200, 'DELETE is not succesful!')
        
    def test_search(self):
        '''get the id of the last post'''
        body = {'searchTerm': 'caged'}
        res = self.client().post('/search', json=body)
        data = json.loads(res.data)
        self.assertTrue((len(data['questions'])), '1')

    def test_get_quizzes(self):
        body= {
            'quiz_category':{
                'id': 1 
            },  
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=body)
        data = json.loads(res.data)
        self.assertEqual((data['category_']), 1, 'Category do not match for the quizzes!')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
