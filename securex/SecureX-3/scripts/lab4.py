#############################################################################
#                                                                           #
#       Lab4 REST API Server                                                #
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
import requests

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


# Update Script To Reflect Lab Requirements
@app.route('/example/', methods=['GET', 'POST'])
def relay():
    """
    Flask API route for Cisco Live Python Lab4

    Each call will be checked to determine the method and provide appropriate functionality
    :return: json object and appropriate status code
    """
    if not check_token(request.headers):
        return create_response({'authentication': 'failed'}, 401)
    remote_url = 'https://jsonplaceholder.typicode.com/users/'
    if request.method == 'INSERT METHOD':
        response = requests.request(request.method, url=remote_url)
        return create_response(response.json(), response.status_code)
    elif request.method == 'INSERT METHODT':
        data = json.loads(request.data)
        response = requests.request(request.method, url=remote_url, data=data)
        return create_response(response.json(), response.status_code)


if __name__ == '__main__':
    """
    Simple logic to determine if this script is being run directly, will not execute if imported by another script
    """
    app.run(debug=False, host='0.0.0.0', port=7000)
