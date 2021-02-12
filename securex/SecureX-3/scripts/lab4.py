#############################################################################
#                                                                           #
#       Lab3 REST API Server                                                #
#                                                                           #
#       Python Flask HTTP Web Server                                        #
#                                                                           #
#       Small web server showcasing how to create a REST API and            #
#       make it interact with backend applications and data structures.     #
#       Here the basic structure of the application will be configured      #
#       along with WSGI and CORS, although they will not be required for    #
#       the lab portion. A simulated token is added to show how to work     #
#       with them. A single route takes all HTTP methods and then uses if   #
#       statements to determine what kind of method it is and takes         #
#       appropriate action. The last call is what actually starts the       #
#       server on the desired port.                                         #
#                                                                           #
#       Author: Brennan Bouchard                                            #
#                                                                           #
#############################################################################

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import json
import requests
# Local Python Files That will be imported to simulate backed application and mock database
import backend_app
import response_json

# Flask Web Server Setup and CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"Access-Control-Allow-Origin": "*"}})
app.wsgi_app = ProxyFix(app.wsgi_app)

# Token that will be referenced in API header

example_token = 'SEVT'


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


# Update Script To Reflect Lab Requirements
@app.route('/YOUR-API-NAME/', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def relay():
    """
    Flask API route for SEVT Python Lab4

    Each call will be checked to determine the method and provide appropriate functionality
    :return: json object and appropriate status code
    """
    if not check_token(request.headers):
        return create_response({'authentication': 'failed'}, 401)
    remote_url = 'https://jsonplaceholder.typicode.com/users/'
    if request.method == 'UPDATE APPROPRIATE METHOD HERE':
        response = requests.request(request.method, url=remote_url)
        return create_response(response.json(), response.status_code)
    elif request.method == 'Update APPROPRIATE METHOD HERE':
        data = json.loads(request.data)
        response = requests.request(request.method, url=remote_url, body=data)
        return create_response(response.json(), response.status_code)


if __name__ == '__main__':
    """
    Simple logic to determine if this script is being run directly, will not execute if imported by another script
    """
    app.run(debug=False, host='0.0.0.0', port=7000)
