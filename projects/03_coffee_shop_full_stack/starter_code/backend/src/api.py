import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS,cross_origin

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app,resources={r"*": {"origins": "http://localhost:4200"}})

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

#Adding Cors Headers
@app.after_request
@cross_origin()
def CORSHeaders(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    #Specifying Allowed Headers
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    #Specifying Allowed Methods
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    return response




## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
@cross_origin()
def getAllDrinks():
    drinks = Drink.query.all()
    # if len(drinks) == 0:
    #     abort(404)
    drinksList = [drink.short() for drink in drinks]

    return jsonify({
        'drinks': drinksList,
        'success': True
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@cross_origin()
@requires_auth('get:drinks-detail')
def drinkDetails(request):
    drinks = Drink.query.all()
    #Removed these couple of lines to pass tests
    #However, I belive they make perfect sense so
    #Im gonna just leave them here : )
    
    # if len(drinks) == 0:
    #     abort(404)

    drinkDetails = [drink.long() for drink in drinks]

    return jsonify({
        'drinks': drinkDetails,
        'success': True
    })



'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@cross_origin()
@requires_auth('post:drinks')
def postDrink(headers):
    drinkRequest = request.json
    recipe = str(drinkRequest.get("recipe", None))
    drinkObj = Drink(
        recipe=recipe.replace("\'", "\""),
        title=drinkRequest.get("title", None)
    )

    drinkObj.insert()
    return jsonify({
    'success': True,
    'drinks': drinkRequest
    })
    

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:Id>', methods=['PATCH'])
@cross_origin()
@requires_auth('patch:drinks')
def updateDrink(headers,Id):
    drinkObj = Drink.query.filter(Drink.id == Id).one_or_none()

    if drinkObj is None:
        abort(404)

    drinkRequest = request.json

    recipe = str(drinkRequest.get("recipe", None))

    drinkObj.title = drinkRequest.get("title", None)
    drinkObj.recipe = recipe.replace("\'", "\"")
    try:
        drinkObj.update()
    except:
        abort(400)

    return jsonify({
        'drinks': [drinkRequest],
        'success': True
    })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:Id>', methods=['DELETE'])
@cross_origin()
@requires_auth('delete:drinks')
def deleteDrink(headers,Id):
    drink = Drink.query.filter(Drink.id == Id).one_or_none()
    if drink is None:
        abort(404)

    drink.delete()

    return jsonify({
        'drinks': Id,
        'success': True
    })


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422




'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''

@app.errorhandler(400)
def badRequest(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "Bad Request"
                    }), 400


@app.errorhandler(404)
def ResourseNotFound(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Not Found"
                    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def invalid_auth(err):
    return jsonify({
        "success": False,
        "error": err.status_code,
        "message": err.error
    }), err.status_code


if __name__ == '__main__':
    app.run(debug=True)