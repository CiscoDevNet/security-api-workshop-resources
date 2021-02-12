#############################################################################
#                                                                           #
#       Example Python Application Backend                                  #
#                                                                           #
#       Demonstrates how API calls from server or client can                #
#       directly interact with backend scripts to trigger automated         #
#       actions                                                             #
#                                                                           #
#                                                                           #
#       Author: Brennan Bouchard                                            #
#                                                                           #
#############################################################################

# import sample dictionary
import response_json


def add_to_response_json(data):
    """
    Function to update the response dictionary so long as the data type
    being sent is of dictionary type.

    :param data: dictionary to be added to response
    :return: the updated response dictionary
    """
    if type(data) == dict:
        response_json.response.update(data)
        return response_json.response
    return {'update': 'failed', 'reason': 'data provided was not formatted as json'}


def update_response_json(user, data):
    """
    Function to update existing user so long as the data type
    being sent is of dictionary type and user is of string type.

    :param data: dictionary to be added to response
    :return: the updated response dictionary
    """
    if type(data) == dict and type(user) == str:
        if user in data.keys():
            data = data[user]
        response_json.response[user] = data
        return response_json.response
    return {'update': 'failed',
            'reason': 'data provided incorrectly formatted. \
                the data must be json formatted, and <user> must be of type string'}


def delete_from_response_json(user):
    """

    :param user:
    :return:
    """
    if type(user) == str:
        try:
            response_json.response.pop(user)
            return response_json.response
        except KeyError:
            return {'error': 'user not in database'}
    return {'error': 'user must be a string'}


if __name__ == '__main__':
    initial_data = response_json.response
    print(initial_data)
    create = add_to_response_json({'ssquarpants': {
        'first_name': 'Spongebob',
        'last_name': 'Squarepants',
        'city': 'Bikini Bottom'
    }})
    print(create)
    update = update_response_json({'ssquarpants', {
        'first_name': 'Spongebob',
        'last_name': 'Squarepants',
        'city': 'Sahara Desert'
    }})
    print(update)
    removed = delete_from_response_json('ssquarpants')
    print(removed)
