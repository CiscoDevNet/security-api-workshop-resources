#############################################################################
#                                                                           #
#       Lab1 REST API Client                                                #
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

#  import requests
import json


def rest(method, url, cookie, data, headers={}, verify=True):
    """
    Generic API client function that can be passed any HTTP verb and appropriate attributes
    :param method: - The HTTP verb desired
    :param url: - the full URL of target and URI
    :param headers: - JSON representation of header dictionary object
    :param cookie: - JSON representation of cookie dictionary object
    :param data: - JSON representation of payload dictionary object
    :param verify: Boolean value to perform strict certificate checks
    :return: returns the entire request object
    """
    return requests.request(method=method, url=url, headers=headers, cookies=cookie,
                            data=json.dumps(data), verify=verify)


def get(url, headers={}, verify=True):
    """
    GET API client function that performs HTTP GET when passed appropriate arguments
    :param url: - the full URL of target and URI
    :param headers: - JSON representation of header dictionary object
    :param verify: Boolean value to perform strict certificate checks
    :return: returns the payload of the request
    """
    data = requests.get(url=url, headers=headers, verify=verify)
    if data.status_code == 200:
        return data


def post(url, headers={}, data={}, verify=True):
    """
    POST API client function that performs HTTP POST when passed appropriate arguments
    :param url: - the full URL of target and URI
    :param headers: - JSON representation of header dictionary object
    :param data: - JSON representation of payload dictionary object
    :param verify: Boolean value to perform strict certificate checks
    :return: returns the payload of the request
    """
    data = requests.post(url=url, data=json.dumps(data), headers=headers, verify=verify)
    if data.status_code == 201:
        return data


def put(url, headers={}, data={}, verify=True):
    """
    PUT API client function that performs HTTP PUT when passed appropriate arguments
    :param url: - the full URL of target and URI
    :param headers: - JSON representation of header dictionary object
    :param data: - JSON representation of payload dictionary object
    :param verify: Boolean value to perform strict certificate checks
    :return: returns the payload of the request
    """
    data = requests.put(url=url, data=data, headers=headers, verify=verify)
    if data.status_code == 200:
        return data


def delete(url, headers={}, verify=True):
    """
    DELETE API client function that performs HTTP DELETE when passed appropriate arguments
    :param url: - the full URL of target and URI
    :param headers: - JSON representation of header dictionary object
    :param verify: Boolean value to perform strict certificate checks
    :return: returns the payload of the request
    """
    data = requests.delete(url=url, headers=headers, verify=verify)
    if data.status_code == 200:
        return data


if __name__ == '__main__':
    """
     Simple logic to determine if this script is being run directly, will not execute if imported by another script
    """
    full_url = 'https://jsonplaceholder.typicode.com/users'
    response = get(full_url, {}, True)
    response_data = json.loads(response.content)
    print('Response Status Code:' + str(response.status_code))
    print('Type of Response Data: ' + str(type(response_data)) + '\n')
    print('Printing User Data: \n')
    for d in response_data:
        print('ID: ' + str(d['id']))
        print('Name: ' + d['name'])
        print('Email: ' + d['email'])
        print('\n')
    print('\n')

