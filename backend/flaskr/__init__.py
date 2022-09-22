# from crypt import methods
from crypt import methods
import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def question_pagination(req, question):
  page = req.args.get('page', 1, type=int)
  start = (page-1)*QUESTIONS_PER_PAGE
  end = start+QUESTIONS_PER_PAGE
  qlist =[q.format() for q in question]
  questions = qlist[start:end]
  return questions



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
      response.headers.add(
          "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
      )
      response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
      )
      return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def getCategory():
      category = Category.query.order_by(Category.id).all()
      cat_list = [cat.format() for cat in category]

      if (len(cat_list))==0:
        abort(404)
      print(category)
      return jsonify({
        'success': True,
        'categories': cat_list,
        'total' : len(cat_list)
      })

    @app.route('/categories', methods=['POST'])
    def post_categories():
      body = request.get_json()
      new_category = body.get('category')

      try:
        category = Category(type = new_category)
        category.insert()

        return jsonify({
          'success':True,
          'created': category.id,
          'total_categories': len(Category.query.all())

        })
      except: 
        abort(422)
     
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get():
      question = Question.query.order_by(Question.id).all()
      question_page = question_pagination(request, question)


      # if (len(question_page)==0):
      #   abort(422)
      return jsonify({
        'success': True,
        'questions': question_page
        
        
      })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_by_id(id):
      try:
        question = Question.query.get(id)
        question.delete()
      except:
        abort(422)
      
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def post_question():
      body = request.get_json()

      q = body.get('question')
      a = body.get('answer')
      c = body.get('category')
      d = body.get('difficulty')

      try:
        question = Question(question=q, answer=a, 
        category=c, difficulty=d)
        question.insert()

        return jsonify({
          'success': True,
          'message': question.id,
          'total_questions': len(Question.query.all())
          })
      except:
        abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/question', methods=['GET'])
    def search_questions():
      search = request.args.get('search',  type=str)
      
      if search == '':
        return
      try:
        question = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
        
        return jsonify({
            'success': True,
            'questons': [q.format() for q in question],
            'total': len(question)

        })
      except:
        abort(422)
      
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/questions/<int: categorry_id>/questions')
    def based_on_category(category_id):
      try:
        questions = Question.query.filter(Question.category== (Category.query.get(category_id).one().type))
        return jsonify({
          'success': True,
          'question': [q.format() for q in questions],
          'total_questions': len([q.format() for q in questions])
        })
      except:
        abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    app.route('/quiz', methods=['POST'])
    def quizzzes():
      try:
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
        category_id = quiz_category['id']

        if category_id == 0:
              questions = Question.query.filter(Question.id.notin_(previous_questions), 
              Question.category == category_id).all()
        else:
          questions = Question.query.filter(Question.id.notin_(previous_questions), 
          Question.category == category_id).all()
        question = None
        if(questions):
          question = random.choice(questions)

        return jsonify({
'         success': True,
          'question': question.format()
            })
      except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
   
    @app.errorhandler(400)
    def bad_request(e):
      return(
        jsonify({
          'success': False, 
          'error': 400,
          'message': 'bad request'
          }),
            400
        )

    @app.errorhandler(404)
    def not_found(e):
      return( 
        jsonify({
          'success': False, 
          'error': 404,'message': 
          'resource not found'
          }),
            404
        )

    @app.errorhandler(422)
    def unprocessed(e):
      return(
        jsonify({
          'success': False, 
          'error': 422,'message': 
          'request cannot be processed'
          }),
            422

        )

    @app.errorhandler(405)
    def not_allowed(e):
      return(
        jsonify({'success': False, 
          'error': 405,
          'message': 'method not alllowed'
          }), 405
          )
    return app

