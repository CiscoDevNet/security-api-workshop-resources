#############################################################################
#                                                                           #
#       Lab3 REST API Server                                                #
#                                                                           #
#       Python Flask HTTP Web Server                                        #
#                                                                           #
#       Small web server showcasing how to create a REST API and            #
#       make it interact with backend applications and data structures.     #
#       A simulated token is added to show how to work                      #
#       with them. A single route takes all HTTP methods and then uses if   #
#       statements to determine what kind of method it is and takes         #
#       appropriate action. The last call is what actually starts the       #
#       server on the desired port.                                         #
#                                                                           #
#       Author: Brennan Bouchard                                            #
#                                                                           #
#############################################################################

from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import json
# Local Python Files That will be imported to simulate backed application and mock database
import backend_app
import response_json

# Flask Web Server Setup and CORS

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Token that will be referenced in API header

example_token = 'Cisco-Live'


def check_token(head):
    """
    Function to check for API token in header and return true if it exists and false if it does not

    :param head: the API header
    :return: boolean as to whether the token matches
    """
    try:
        if head['token'] == example_token:
            return True
        else:
            return False
    except KeyError:
        return False


def create_response(data, status):
    """
    Function to build response object with payload as data and status as the HTTP status code

    :param data: json data to be returned
    :param status: HTTP status code
    :return: response object
    """
    resp = jsonify(data)
    resp.status_code = status
    return resp


@app.route('/ciscolive/', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def ciscolive():
    """
    Flask API route for all methods to /ciscolive endpoint

    Each call will be checked to determine the method and provide appropriate functionality
    :return: json object and appropriate status code
    """
    if not check_token(request.headers):
        return create_response({'authentication': 'failed'}, 401)
    if request.method == 'GET':
        return create_response(response_json.response, 200)
    elif request.method == 'POST':
        data = json.loads(request.data)
        return create_response(backend_app.add_to_response_json(data), 200)
    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            user = request.args['user']
        except KeyError as k:
            return create_response({'error': k}, 400)
        data = json.loads(request.data)
        return create_response(backend_app.update_response_json(user, data), 200)
    elif request.method == 'DELETE':
        try:
            user = request.args['user']
        except KeyError as k:
            return create_response({'error': k}, 400)
        return create_response(backend_app.delete_from_response_json(user), 200)


@app.route('/ciscolive/<user>/', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def ciscolive_user(user):
    """
    Flask API route for all methods to /ciscolive/<user>/ endpoint

    Each call will be checked to determine the method and provide appropriate functionality
    :return: json object and appropriate status code
    """
    if not check_token(request.headers):
        return create_response({'authentication': 'failed'}, 401)
    if user not in response_json.response.keys():
        create_response({'error': 'user not in database'}, 400)
    if request.method == 'GET':
        return create_response(response_json.response[user], 200)
    elif request.method == 'PUT' or request.method == 'PATCH':
        data = json.loads(request.data)
        return create_response(backend_app.update_response_json(user, data), 200)
    elif request.method == 'DELETE':
        return create_response(backend_app.delete_from_response_json(user), 200)


if __name__ == '__main__':
    """
    Simple logic to determine if this script is being run directly, will not execute if imported by another script
    """
    app.run(debug=False, host='0.0.0.0', port=7000)
