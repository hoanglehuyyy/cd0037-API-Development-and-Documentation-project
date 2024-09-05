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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions/?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_get_questions_in_specified_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_404_get_questions_in_invalid_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_search_questions(self):
        res = self.client().post('questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_delete_not_exist_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
        new_question = {
            'question': 'Test question',
            'answer': 'Test answer',
            'category': 2,
            'difficulty': 5
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_405_question_creation_not_allowed(self):
        new_question = {
            'question': 'Test question',
            'answer': 'Test answer',
            'category': 2,
            'difficulty': 5
        }
        res = self.client().post('/questions/100', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_400_question_creation_miss_question(self):
        new_question = {
            'question': '',
            'answer': 'Test answer',
            'category': 2,
            'difficulty': 5
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_400_question_creation_miss_answer(self):
        new_question = {
            'question': 'Test question',
            'answer': '',
            'category': 2,
            'difficulty': 5
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_play_quiz(self):
        quiz = {
            'previous_questions': [5, 12],
            'quiz_category': {
                'id': 4,
                'type': 'History'
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test__no_questions_available_for_quiz(self):
        quiz = {
            'previous_questions': [5, 9, 12, 23],
            'quiz_category': {
                'id': 4,
                'type': 'History'
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()