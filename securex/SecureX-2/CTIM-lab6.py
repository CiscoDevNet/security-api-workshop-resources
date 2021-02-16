#!/usr/lib/python3
import os
import sys
import requests
import json
from datetime import datetime,timedelta,date


'''
  Do an HTTP GET given URL with given headers and return the returned JSON, except otherwise
'''
def get(url,headers): 
    print("API GET url {} headers {}".format(url,str(headers)))  
    print("\nWaiting for API response...\n")    
    r = requests.get(url=url,headers=headers,verify=True)
    status_code = r.status_code
    if  (status_code / 100) == 2:
        json_response = json.loads(r.text)
        return json_response
    else:
        errorstring = "Error in get url:{} statuscode:{} text {}".format(url,str(status_code),r.text)                                               
        raise ValueError(errorstring)                                

'''
Do a HTTP POST given (URL, headers) and return the JSON, except otherwise
'''

def post(url,headers,data,auth=""):

    print("API POST url {} headers {} data {}".format(url,str(headers),str(data)))
    print("\nWaiting for API response...\n") 
    r = requests.post(url,data=data,headers=headers,auth=auth,verify=True)
    if r.status_code // 100 == 2:
        json_response = json.loads(r.text)
        return json_response
    else:
        errorstring = "Error in post {} {} {}".format(url,str(r.status_code),r.text)
        raise ValueError(errorstring)    


'''
Main function to be run
Assumes you have a file called creds.json in the same directory, with this format
   {
       "client_id": " <.... client_id acquired from your SecureX environment> ",
       "client_password":l <.... client password aquired from your SecureX environment>"
   }
'''
def main(argv):

    '''
    Get input to this script:  
    observable raw text, e.g. internetbadguys.com
    '''
    
    RAW_OBSERVABLES = ' '.join(argv[0:])
    if not RAW_OBSERVABLES:
        print("no observables given!")
        sys.exit()
    
    print("Raw Observable is {}".format(RAW_OBSERVABLES))

    print("Opening creds.json")
    try:
        creds = json.loads(open("creds.json").read())
        CLIENT_ID = creds["client_id"]
        CLIENT_PASSWORD = creds["client_password"]
    except Exception:
        print("Error - Failed to extract client_id and client_password from file creds.json - exiting...")
        sys.exit()
    
    print("Extracted client_id and client_password from file creds.json")
    input("\nPress Enter to continue with the next step - to use the client_id and client_password to acquire a temporary ACCESS TOKEN\n")
   
    '''
        Define the headers, data, and url to go with the POST that will acquire the access token.
        The format of the headers and token are defined in the API, and can be learned from the Swagger client.
        Then acquire the access token and keep it for further requests.
    '''
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
    }
    data = {
            'grant_type': 'client_credentials'
    }
    url = 'https://visibility.amp.cisco.com/iroh/oauth2/token'

    response = post(url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_PASSWORD))
    print("Acquire ACCESS TOKEN....")
    print("The API returned the response:")
    print(json.dumps(response,indent=4,sort_keys=True))
    try: 
        ACCESS_TOKEN = response["access_token"]
    except Exception:
        print("Failed to get ACCESS_TOKEN - exiting")
        sys.exit()
    print("ACCESS_TOKEN is {}".format(ACCESS_TOKEN))

    input("\nPress Enter to continue with the next step - to get the CTIM observables in JSON format from our raw observables\n")

    '''
    Get the CTIM observable JSON format from any observable in our raw observables
    '''
    BEARER_TOKEN = 'Bearer ' + ACCESS_TOKEN
    headers = {
        'Authorization': BEARER_TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = json.dumps({"content":RAW_OBSERVABLES})
    url = 'https://visibility.amp.cisco.com/iroh/iroh-inspect/inspect'
    OBSERVABLES = post(url, headers=headers, data=data)
    print("Observables returned by the API response are:")
    print(json.dumps(OBSERVABLES,indent=4,sort_keys=True))

    input("\nPress Enter to continue with the next step - to enrich and deliberate the observables\n")

    '''
    Enrich and Deliberate  (means get more info from) the observables from previous step
    '''
    url = 'https://visibility.amp.cisco.com/iroh/iroh-enrich/deliberate/observables'
    data = json.dumps(OBSERVABLES)
    response = post(url, headers=headers, data=data)
    print("Response returned by API is")
    print(json.dumps(response,indent=4,sort_keys=True))

    input("\nPress Enter to continue with the next step - to get even more info from observables\n")

    '''
    Get Even more info from Observables
    '''
    url = 'https://visibility.amp.cisco.com/iroh/iroh-enrich/observe/observables'
    response = post(url, headers=headers, data=data)
    print("Response returned by API is")
    print(json.dumps(response,indent=4,sort_keys=True))

    input("\nPress Enter to continue with the next step - to get the response actions of the observables\n")

    '''
    Get the Response Actions for the Observables
    '''
    url = 'https://visibility.amp.cisco.com/iroh/iroh-response/respond/observables'
    response = post(url, headers=headers, data=data)
    print("Response returned by API is")
    print(json.dumps(response,indent=4,sort_keys=True))

    input("\nPress Enter to continue with the next step - to create a casebook with the observables\n")
    '''
    Create a casebook with the observables
    '''
    d = date.today()
    start_date = d.strftime("%Y-%m-%d")
    casebook_obj_json = {}
    casebook_obj_json["type"] = "casebook"
    casebook_obj_json["title"] = "CTIM LAB <CCO-ID-HERE>:" + start_date
    casebook_obj_json["texts"] = []
    casebook_obj_json["observables"] = OBSERVABLES
    casebook_obj_json["short_description"] = "Something has happened!"
    casebook_obj_json["description"] = "Cats are cute!"
    casebook_obj_json["schema_version"] = "1.0.11"
    casebook_obj_json["timestamp"] = start_date
    casebook_obj_json["source"] = "ao"
    casebook_obj_json["tlp"] = "green"
    data = json.dumps(casebook_obj_json)

    url = 'https://private.intel.amp.cisco.com/ctia/casebook'
    response = post(url,headers=headers,data=data)
    print("Response returned by API is")
    print(json.dumps(response,indent=4,sort_keys=True))

    print("\nCongratulations, you have completed the lab!\n")

if __name__ == "__main__":
    main(sys.argv[1:])

