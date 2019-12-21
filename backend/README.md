# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


API DOCUMEN TATION 
```
 

Endpoints
GET '/questions'
POST '/questions'
DELETE '/questions
GET '/categories'
GET '/categories/<int:category_id>/questions'
POST '/search'
GET '/quizzes'


GET '/questions'
- Fetches all the questions if pagination is not defined. Page={NUM} returns 10 questions per page. 
- Request Arguments: None, page{NUM}
- Returns: An object with all the categories, current category, and questions available, or paginated results of the   same. 
- Error(404) is returned if the quesitions are not found when paginated search is sent.
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },

POST '/questions'
- Posts questions with the following values - category(int), question, answer, and difficulty(int).
- Request Arguments: question, answer, category, difficulty.   
- Returns: If successfully posted returns an object that has the posting parameters, and success code of 200
          -If posting is not successful, returns 'success: False' and the appropriate status code(404, and 500)
  {
        "question": {
            "answer": "Mt. Everest",
            "category": 3,
            "difficulty": 1,
            "question": "What is the highest mountain in the world?"
        },
        "status": 200,
        "success": true
}      

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
    { '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
}

GET '/categories/<int:category_id>/questions'
- Fetches questions within a category. 
- Parameter(s): <int:category_id> (required)
- Pagination: optional

- Returns: An object of questions within the category.
{
	'current_category': 1,
	'questions': [{
		'answer': 'The Liver',
		'category': 1,
		'difficulty': 4,
		'id': 20,
		'question': 'What is the heaviest organ in the human body?'
	}, {
		'answer': 'Alexander Fleming',
		'category': 1,
		'difficulty': 3,
		'id': 21,
		'question': 'Who discovered penicillin?'
	}, {
		'answer': 'Blood',
		'category': 1,
		'difficulty': 4,
		'id': 22,
		'question': 'Hematology is a branch of medicine involving the study of what?'
	}, {
		'answer': 'Tesla',
		'category': 1,
		'difficulty': 1,
		'id': 26,
		'question': 'who invented AC'
	}, {
		'answer': 'Nepal',
		'category': 1,
		'difficulty': 1,
		'id': 30,
		'question': 'where is kathmandu?'
	}, {
		'answer': 'wright brothers',
		'category': 1,
		'difficulty': 1,
		'id': 33,
		'question': 'who invented airplanes?'
	}],
	'total_questions': 6
}



```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
