#############################################################################
#                                                                           #
#       Lab2 REST API Client                                                #
#                                                                           #
#       Generic requests call allowing for any available operation          #
#                                                                           #
#       Separate function call for each verb along with generic call        #
#       If the script is run directly, rather than imported it will         #
#       it will perform an HTTP GET operation to a testing web server.      #
#       The response obtained will then print details to the console        #
#                                                                           #
#       Author: Brennan Bouchard                                            #
#                                                                           #
#############################################################################

import requests
import json


def get(url, verify=True):
    """
    GET API client function that performs HTTP GET when passed appropriate arguments
    :param url: - the full URL of target and URI
    :param headers: - JSON representation of header dictionary object
    :param verify: Boolean value to perform strict certificate checks
    :return: returns the payload of the request
    """
    data = requests.get(url=url, verify=verify)
    if data.status_code == 200:
        return data


def post(url, data={}, verify=True):
    """
    POST API client function that performs HTTP POST when passed appropriate arguments
    :param url: - the full URL of target and URI
    :param headers: - JSON representation of header dictionary object
    :param data: - JSON representation of payload dictionary object
    :param verify: Boolean value to perform strict certificate checks
    :return: returns the payload of the request
    """
    data = requests.post(url=url, data=json.dumps(data), verify=verify)
    if data.status_code == 201:
        return data


def put(url, data={}, verify=True):
    """
    PUT API client function that performs HTTP PUT when passed appropriate arguments
    :param url: - the full URL of target and URI
    :param headers: - JSON representation of header dictionary object
    :param data: - JSON representation of payload dictionary object
    :param verify: Boolean value to perform strict certificate checks
    :return: returns the payload of the request
    """
    data = requests.put(url=url, data=data, verify=verify)
    if data.status_code == 200:
        return data


def delete(url, verify=True):
    """
    DELETE API client function that performs HTTP DELETE when passed appropriate arguments
    :param url: - the full URL of target and URI
    :param headers: - JSON representation of header dictionary object
    :param verify: Boolean value to perform strict certificate checks
    :return: returns the payload of the request
    """
    data = requests.delete(url=url, verify=verify)
    if data.status_code == 200:
        return data


new_user = {
    'id': 11,
    'name': 'Darth Vader',
    'email': 'vaddar@cisco.com'
}


update_user = {
    'id': 4,
    'phone': '1-555-555-5555',
}


if __name__ == '__main__':
    """
     Simple logic to determine if this script is being run directly, will not execute if imported by another script
    """
    full_url = 'https://jsonplaceholder.typicode.com/users'
    # Add requested code below to complete the lab


