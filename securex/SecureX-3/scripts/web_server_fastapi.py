#############################################################################
#                                                                           #
#       REST-SEVT Web Server Using FastAPI                                  #
#                                                                           #
#       Listens for connections using /sevt endpoint, validates token       #
#       and forwards operation to internal resource.                        #
#                                                                           #
#                                                                           #
#                                                                           #
#       Author: Brennan Bouchard                                            #
#                                                                           #
#############################################################################

from typing import Optional, Dict
from fastapi import FastAPI, Request, Response, status
from fastapi.openapi.utils import get_openapi
import response_json


app = FastAPI()
example_token = 'API-TOKEN'


def check_token(head):
    return True
    if head['relay-token'] == token:
        return True
    else:
        return False


@app.get('/sevt')
def get_sevt(r: Request, resp: Response):
    """
        SEVT web server route for GET request.
        :param r Request object, provides access to method, headers & cookies:
        :param resp Response Object used for modification of status code:
        :return returns the content of the internal resources response:
    """
    if check_token(r.headers):
        resp.status_code = status.HTTP_200_OK
        return response_json.response
    resp.status_code = status.HTTP_401_UNAUTHORIZED
    return


@app.post('/sevt')
def post_sevt(r: Request, resp: Response, body: Dict):
    """
        SEVT web server route for POST request.
        :param r Request object, provides access to method, headers & cookies:
        :param resp Response Object used for modification of status code:
        :param body Payload for call to internal respource:
        :return returns the content of the internal resources response:
    """
    if sevt.check_token(r.headers):
        resp.status_code = status.HTTP_200_OK
        return backend_app.add_to_response_json(body)
    resp.status_code = status.HTTP_401_UNAUTHORIZED
    return


@app.put('/sevt')
def put_sevt(r: Request, resp: Response, body: Dict, user=''):
    """
        SEVT web server route for PUT request.
        :param r Request object, provides access to method, headers & cookies:
        :param resp Response Object used for modification of status code:
        :param body Payload for call to internal respource:
        :param user URL argument for the desired user:
        :return returns the content of the internal resources response:
        """
    if sevt.check_token(r.headers):
        resp.status_code = status.HTTP_200_OK
        return backend_app.update_response_json(user, body)
    resp.status_code = status.HTTP_401_UNAUTHORIZED
    return


@app.patch('/sevt')
def patch_sevt(r: Request, resp: Response, body: Dict, user=''):
    """
        SEVT web server route for PATCH request.
        :param r Request object, provides access to method, headers & cookies:
        :param resp Response Object used for modification of status code:
        :param body Payload for call to internal respource:
        :param user URL argument for the desired user:
        :return returns the content of the internal resources response:
        """
    if sevt.check_token(r.headers):
        resp.status_code = status.HTTP_200_OK
        return backend_app.update_response_json(user, body)
    resp.status_code = status.HTTP_401_UNAUTHORIZED
    return


@app.delete('/sevt')
def delete_sevt(r: Request, resp: Response, user=''):
    """
        SEVT web server route for DELETE request.
        :param r Request object, provides access to method, headers & cookies:
        :param resp Response Object used for modification of status code:
        :param user URL argument for the desired user:
        :return returns the content of the internal resources response:
        """
    if sevt.check_token(r.headers):
        resp.status_code = status.HTTP_200_OK
        return backend_app.delete_from_response_json(user)
    resp.status_code = status.HTTP_401_UNAUTHORIZED
    return


swagger_token = {
    'required': True,
    'schema': {
        'type': 'string'
    },
    'name': 'sevt-token',
    'in': 'header'
}
'''
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="REST-SEVT API Proxy",
        version="1.0.0",
        description="HTTP Proxy For REST Operations",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "data:image/jpeg;base64,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"
    }
    openapi_schema['paths']['/sevt']['get']['parameters'].append(swagger_token)
    openapi_schema['paths']['/sevt']['post']['parameters'].append(swagger_token)
    openapi_schema['paths']['/sevt']['put']['parameters'].append(swagger_token)
    openapi_schema['paths']['/sevt']['patch']['parameters'].append(swagger_token)
    openapi_schema['paths']['/sevt']['delete']['parameters'].append(swagger_token)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
'''

