from authlib.jose import jwt
from authlib.jose.errors import BadSignatureError, DecodeError
from flask import current_app, jsonify, request
from datetime import datetime, timedelta
from errors import AuthorizationError, InvalidArgumentError
import time

def get_auth_token():
    """
    Parse and validate incoming request Authorization header.

    NOTE. This function is just an example of how one can read and check
    anything before passing to an API endpoint, and thus it may be modified in
    any way, replaced by another function, or even removed from the module.
    """
    expected_errors = {
        KeyError: 'Authorization header is missing',
        AssertionError: 'Wrong authorization type'
    }
    try:
        scheme, token = request.headers['Authorization'].split()
        assert scheme.lower() == 'bearer'
        return token
    except tuple(expected_errors) as error:
        raise AuthorizationError(expected_errors[error.__class__])


def get_jwt():
    """
    Parse the incoming request's Authorization Bearer JWT for some credentials.
    Validate its signature against the application's secret key.

    NOTE. This function is just an example of how one can read and check
    anything before passing to an API endpoint, and thus it may be modified in
    any way, replaced by another function, or even removed from the module.
    """

    expected_errors = {
        KeyError: 'Wrong JWT payload structure',
        TypeError: '<SECRET_KEY> is missing',
        BadSignatureError: 'Failed to decode JWT with provided key',
        DecodeError: 'Wrong JWT structure'
    }
    token = get_auth_token()
    try:
        return ""
    except tuple(expected_errors) as error:
        raise AuthorizationError(expected_errors[error.__class__])


def get_json(schema):
    """
    Parse the incoming request's data as JSON.
    Validate it against the specified schema.

    NOTE. This function is just an example of how one can read and check
    anything before passing to an API endpoint, and thus it may be modified in
    any way, replaced by another function, or even removed from the module.
    """

    data = request.get_json(force=True, silent=True, cache=False)

    '''
    message = schema.validate(data)

    if message:
        raise InvalidArgumentError(message)
    '''
    return data


def jsonify_data(data):
    return jsonify({'data': data})


def jsonify_errors(data):
    return jsonify({'errors': [data]})
    
def current_date_time():
    current_time = datetime.utcnow()
    current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return(current_time)
    
def date_plus_x_days(nb):   
    current_time = datetime.utcnow()
    start_time = current_time + timedelta(days=nb)
    timestampStr = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return(timestampStr)
    
def epoch_date(date):
    pattern = '%Y-%m-%d %H:%M:%S'
    date_time = date +' 01:01:01'
    epoch_int = int(time.mktime(time.strptime(date_time, pattern)))
    epoch=str(epoch_int)+'000'
    #print(epoch) 
    return(epoch)
    
def epoch_datetime(datetime):
    pattern = '%Y-%m-%d %H:%M:%S'
    date_time = datetime
    epoch_int = int(time.mktime(time.strptime(date_time, pattern)))
    epoch=str(epoch_int)
    print(cyan(epoch,bold=True)) 
    return(epoch)       
