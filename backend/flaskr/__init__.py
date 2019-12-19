import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys 
import json 

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page -1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_question = questions[start:end]
  return current_question


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})  

  '''
   Use the after_request decorator to set Access-Control-Allow
  '''
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    return response

  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories',methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted_category = {category.id: category.type for category in categories}
    return jsonify({
      'categories': formatted_category,
      'status': 200
      })
     
  
  '''
  An endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint returns a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route('/questions',methods=['GET'])
  def get_questions():
    questions =  Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.type).all()
    formatted_categories = {category.id: category.type for category in categories}
    current_questions = paginate(request, questions) 
    if len(current_questions) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'questions': current_questions,
      'categories': formatted_categories,
      'total_questions': len(questions),
      'current_category': None
    })


  '''
   An endpoint to DELETE question using a question ID.  
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    Question.query.get(id).delete()
    return jsonify({
      'success': True
    })


  '''
  An endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  '''
  @app.route('/questions', methods=['POST'])
  def add_questions():
    question = request.get_json()
    if question['question'] == '':
      error = "Not Complete"
      abort(500)
    try:
      Question(
        question=question['question'],
        answer=question['answer'],
        category=question['category'],
        difficulty=question['difficulty']
        ).insert()
      return jsonify({
        'question': question,
        'success': True,
        'status':200
        })
    except Exception:
      return jsonify({
        'success': False,
        })

  '''
  A POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question.  
  '''

  @app.route('/search', methods=['POST'])
  def search():
   search_term = request.get_json()['searchTerm']
   search_data = Question.query.filter(Question.question.ilike(f'%{search_term}%'))

   return jsonify({
     'questions': [q.format() for q in search_data],
     'current_category': None
   })


  '''
  
  A GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    formatted_questions = [question.format() for question in questions]
    if len(formatted_questions) == 0:
      abort(404)
    return jsonify({
      'questions': formatted_questions,
      'total_questions': len(formatted_questions),
      'current_category': category_id
    })


  '''
  A POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  '''

  @app.route('/quizzes', methods=['POST'])
  def get_quizzes():
    quiz_category = int(request.get_json()['quiz_category']['id'])
    previous_questions = request.get_json()['previous_questions']

    '''create random, and unique question for the category'''
    if quiz_category not in [1,2,3,4,5,6]:
      unique_questions = Question.query.all()
    else:
      unique_questions = Question.query.filter_by(category=quiz_category).filter(Question.id.notin_(previous_questions)).all()

    if len(unique_questions) > 0:
      return jsonify({
        'success': True,
        'question': random.choice([q.format() for q in unique_questions]),
        'category_': quiz_category,
        'previous': [u.question for u in unique_questions]
      })
    else:
      return jsonify({
        'success': True,
        'question': None
      })


  '''
  Error handlers for all expected errors 
  '''
 
  @app.errorhandler(404)
  def not_found_error(error):
      return jsonify({
        "error": 404,
        "message": "Page Not Found"
      }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
        "error": 422,
        "message": "unprocessable entity"
      }), 422

 
  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
        "error": 500,
        "message": "server error"
      }), 500
 

  return app

    
