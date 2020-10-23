#!/usr/bin/env python3

"""
Copyright (c) 2018-2020 Cisco and/or its affiliates.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Script Version 1.2
Python Mission: Create Threat Investigation & Response Automation Workflow

Mission Steps

Step 1. In AMP for Endpoints, get a list of all the events of "Threat Detected" and "Executed Malware" types 
        for a specific computer named `Demo_AMP_Threat_Audit`, capture malicious sha256 associated with the first event.
Missions to complete: MISSION01, MISSION02, MISSION03

Step 2. Isolate infected Computer to perform further investigation and make sure that the action was successful.

Missions to complete: MISSION04

Step 3. In Threat Grid, find all samples, associated with malicious sha256 that you have captured in step 1 
        and look at analysis report for the first sample on the list.
Missions to complete: MISSION05, MISSION06

Step 4. Request all domains for a specific sample in Threat Grid and store them in an array to get more data out of them.

Missions to complete: MISSION07

Step 5. Check all associated domains against Umbrella Investigate to retrieve their status.

Missions to complete: MISSION08, MISSION09, MISSION10

Step 6. Using Umbrella Enforcement, post malware events to the API for processing and optionally adding 
        to a customer's domain lists.
Missions to complete: MISSION11

Step 7. Using Threat Response, inspect if malicious sha256 has been found on our network. 
        Use response capabilities of AMP for Endpoints module to block this malicious file from execution 
        on all Computers in our network.
Missions to complete: MISSION12, MISSION13, MISSION14

Step 8. Use response capabilities of AMP for Endpoints module in CTR to block this malicious file 
        from execution on all Computers in our network.
Missions to complete: MISSION15

Step 9: Uncomment the validation section and submit solution for review.
"""

from datetime import datetime
import json
import sys
from pathlib import Path
import requests
from crayons import blue, green, yellow, white, red
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." ).resolve()
sys.path.insert(0, str(repository_root))

import environment as env
from fjmvlib import *

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Constants

webex_token = env.WEBEX_TEAMS_ACCESS_TOKEN

# MISSION01: Assign the correct computer name to the variable.
# Hint: Refer to Step 1 of the Mission Overview in the lab guide.
amp_computer_name = "MISSION01"

# Functions

def get_amp_computers(
    host=env.AMP.get("host"),
    client_id=env.AMP_CLIENT_ID,
    api_key=env.AMP_API_KEY,
):
    """Get a list of computers from Cisco AMP."""
    print("\n==> Getting computers from AMP")
    # MISSION02: Construct the URL
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    url = f"https://MISSION02"

    response = requests.get(url, verify=False)
    # Consider any status other than 2xx an error
    response.raise_for_status()

    computer_list = response.json()["data"]
    
    return computer_list


def get_amp_events(query_params="",
    host=env.AMP.get("host"),
    client_id=env.AMP_CLIENT_ID,
    api_key=env.AMP_API_KEY,
):
    """Get a list of recent events from Cisco AMP."""
    print("\n==> Getting events from AMP")
    # MISSION04: Construct the URL
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    url = f"https://MISSION04"

    response = requests.get(url, params=query_params, verify=False)
    # Consider any status other than 2xx an error
    response.raise_for_status()

    events_list = response.json()["data"]
    
    return events_list

# method should be 'put', 'get' or 'delete'
def amp_isolation(method, computer_guid,
    host=env.AMP.get("host"),
    client_id=env.AMP_CLIENT_ID,
    api_key=env.AMP_API_KEY,
):
    print(f"\n==> Performing {method} isolation in AMP")
    
    url = f"https://{client_id}:{api_key}@{host}/v1/computers/{computer_guid}/isolation"

    if method == 'get':
        response = requests.get(url, verify=False)
        response.raise_for_status()
    elif method == 'put':
        response = requests.put(url, verify=False)
        if response.status_code == 409:
            print(red("ATTENTION: The computer is already isolated."))
        else:
            response.raise_for_status()
    elif method == 'delete':
        response = requests.delete(url, verify=False)
        response.raise_for_status()
    else:
        print(red("ERROR: Unrecognized REST API Method. Please use 'get', 'put' or 'delete'."))
        sys.exit(1)
    
    isolation_status = response.json()["data"]

    return isolation_status


def threatgrid_search_submissions(
    sha256,
    host=env.THREATGRID.get("host"),
    api_key=env.THREATGRID_API_KEY,
):
    """Search TreatGrid Submissions, by sha256.
    Args:
        sha256(str): Lookup this hash in ThreatGrid Submissions.
        host(str): The ThreatGrid host.
        api_key(str): Your ThreatGrid API key.
    """
    print(white(f"\n==> Searching the ThreatGrid Submissions for sha256: {sha256}"))

    query_parameters = {
        "q": sha256,
        "api_key": api_key,
    }
    
    response = requests.get(
        f"https://{host}/api/v2/search/submissions",
        params=query_parameters,
    )
    # MISSION06: Put proper function to consider any status other than 2xx an error
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    # Put your code here: MISSION06

    submission_info = response.json()["data"]["items"]

    if submission_info:
        print(green("Successfully retrieved data on the sha256 submission"))
    else:
        print(red("Unable to retrieve data on the sha256 submission"))
        sys.exit(1)

    return submission_info


def threatgrid_get_domains(sample_id,
    host=env.THREATGRID.get("host"),
    api_key=env.THREATGRID_API_KEY,
):  
    print(white(f"\n==> Obtaining domains associated with the ThreatGrid Sample ID: {sample_id}"))

    url = f"https://{host}/api/v2/samples/feeds/domains"
    query_params = {
        "sample": sample_id,
        "after": "2020-01-01",
        "api_key": api_key,
    }

    response = requests.get(
        url,
        params=query_params,
    )
    response.raise_for_status()
    
    domains_json = response.json()["data"]["items"]
    domains = []
    if domains_json:
        for item in domains_json:
            if (item["domain"] not in domains):
                domains.append(item["domain"])
    else:
        print(red("Unable to retrieve domains on the sha256 submission. Extend timeframe and try again."))
        sys.exit(1)
    
    return domains


def get_umbrella_domain_status(domain,
    host=env.UMBRELLA.get("inv_url"),
    api_key=env.UMBRELLA_INVESTIGATE_KEY,
):
    print(white(f"\n==> Checking domain against Umbrella Investigate to retrieve its status"))

    url = f"https://{host}/domains/categorization/{domain}?showLabels"

    # MISSION09: Construct authentication headers for Umbrella Investigate
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    headers = {'MISSION09':'MISSION09'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    domain_status = response.json()[domain]["status"]
    
    return domain_status


def post_umbrella_events(blocklist_domains,
    host=env.UMBRELLA.get("en_url"),
    api_key=env.UMBRELLA_ENFORCEMENT_KEY,
):
    print(white(f"\n==> Post malware events to the Umbrella Enforcement API for processing and optionally adding to a customer's domain lists."))
    # MISSION11: Construct the API endpoint to post malware events to the Umbrella Enforcement API
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    url = f"MISSION11"

    headers={'Content-type': 'application/json', 'Accept': 'application/json'}

    # Time for AlertTime and EventTime when domains are added to Umbrella
    time = datetime.now().isoformat()
    data = []
    
    for domain in blocklist_domains:
        obj = {
            "alertTime": time + "Z",
            "deviceId": "ba6a59f4-e692-4724-ba36-c28132c761de",
            "deviceVersion": "13.7a",
            "dstDomain": domain,
            "dstUrl": "http://" + domain + "/",
            "eventTime": time + "Z",
            "protocolVersion": "1.0a",
            "providerName": "Security Platform"
        }
        data.append(obj)

    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.raise_for_status()

    id = response.json()["id"]

    return id, data


def ctr_auth(
    host=env.THREATRESPONSE.get("host"),
    client_id=env.CTR_CLIENT_ID,
    api_key=env.CTR_API_KEY,
):
    print(white("\n==> Authenticating to Cisco Threat Response..."))
    url = f"https://{host}/iroh/oauth2/token"

    headers = {'Content-Type':'application/x-www-form-urlencoded', 'Accept':'application/json'}
    # MISSION12: Construct payload to pass in authentication request to Threat Response
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    payload = {'MISSION12':'MISSION12'}

    response = requests.post(url, headers=headers, auth=(client_id, api_key), data=payload)
    response.raise_for_status()

    access_token = response.json()["access_token"]

    return access_token


def ctr_inspect(access_token, arb_text,
    host=env.THREATRESPONSE.get("host"),
):
    print(white("\n==> Take in block of arbitrary text and return a list of formatted observables as a JSON object..."))
    
    url = f"https://{host}/iroh/iroh-inspect/inspect"

    headers = {"Authorization":f"Bearer {access_token}", 'Content-Type':'application/json', 'Accept':'application/json'}

    inspect_payload = {'content':arb_text}

    inspect_payload = json.dumps(inspect_payload)

    response = requests.post(url, headers=headers, data=inspect_payload)
    response.raise_for_status()

    observables = response.json()

    return observables
    
# MISSION14: Pass to the function properly formatted observables obtained in Step 7.
# env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
def ctr_enrich_observe(access_token, MISSION14,
    host=env.THREATRESPONSE.get("host"),
):
    print(white("\n==> Fetching Sightings about provided observables from CTR modules. Be patient, it may take time..."))
    
    url = f"https://{host}/iroh/iroh-enrich/observe/observables"

    headers = {"Authorization":f"Bearer {access_token}", 'Content-Type':'application/json', 'Accept':'application/json'}

    observe_payload = json.dumps(observable)

    response = requests.post(url, headers=headers, data=observe_payload)
    response.raise_for_status()

    data = response.json()["data"]

    return data


def ctr_enrich_print_scr_report(intel):

    print(white("\n==> Here is what CTR has found:"))

    for module in intel:
        print(white(f"\n==> Module: {module['module']} : {module['module_type_id']}"))
        if module["data"]:
            if module["module"] == "AMP EDR":
                print(blue(f"\n  ==> Count of Indicators: {module['data']['indicators']['count']} "))
                for indicator in module["data"]["indicators"]["docs"]:
                    print(blue(f"  ==> {indicator['description']} : {indicator['tags']}"))
                
                print(blue(f"\n  ==> Count of Sightings: {module['data']['sightings']['count']} "))
                sighting = module['data']['sightings']['docs'][0]
                print(blue(f"  ==> Most recent sighting: {sighting['description']}"))

                if sighting["targets"]:
                    print(blue(f"\n  ==> Targets found: {len(sighting['targets'])}"))
                    target = sighting["targets"][0]
                    print(blue(f"  ==> Most recent target: {target['type']} observed: {target['observed_time']['start_time']}"))
                    for observable in target["observables"]:
                        print(blue(f"  ==> Target {observable['type']} : {observable['value']}"))
                    print(blue(f"  ==> Target OS: {target['os']}"))
            elif module["module"] == "AMP File Reputation":
                for key in module["data"].keys():
                    print(blue(f"  ==> Count of {key}: {module['data'][key]['count']}"))
            elif module["module"] == "AMP Global Intelligence":
                for key in module["data"].keys():
                    print(blue(f"  ==> Count of {key}: {module['data'][key]['count']}"))
        else:
            print(blue("\n==> DO DATA"))


def ctr_response_actions(access_token,observables,
    host=env.THREATRESPONSE.get("host"),
):
    """ POST https://{{ctr_host}}/iroh/iroh-response/respond/observables """

    print(white("\n==> Fetching the list of available response actions and modules for a given observable..."))
    
    url = f"https://{host}/iroh/iroh-response/respond/observables"

    payload = json.dumps(observables)

    headers = {"Authorization":f"Bearer {access_token}", 'Content-Type':'application/json', 'Accept':'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    # Using list comprehentions [obj[key1] for obj in objects if obj[key2] == value]
    actions = response.json()["data"]
    response_url = [action["url"] for action in actions if action["id"] == "amp-add-sha256-scd"]
    
    if not response_url:
        #response_url = None
        print(red(f"ERROR: Required action is not in the list. Remove sha256 from SCD list and try again. Refer to the lab guide for help."))
        sys.exit(1)

    return response_url[0]


def ctr_add_to_amp_scd(access_token, action_url,
    host=env.THREATRESPONSE.get("host"),
):
    print(white("\n==> Adding a malicious sha256 to AMP Simple Custom Detections list named Quarantine..."))
    
    url = f"https://{host}/iroh/iroh-response{action_url}"

    headers = {"Authorization":f"Bearer {access_token}", 'Content-Type':'application/json', 'Accept':'application/json'}

    response = requests.post(url, headers=headers)
    response.raise_for_status()

    return response.status_code


# If this script is the "main" script, run...
if __name__ == "__main__":

    """
    Step 1. In AMP for Endpoints, get a list of all the events of "Threat Detected" and 
    "Executed Malware" types for a specific computer named `Demo_AMP_Threat_Audit`, 
    capture malicious sha256 associated with the first event.
    """
    
    # Hint: If you get stuck at any point, try referring to your Postman solution! 

    print(white(f"\nStep 1"))

    amp_computer_list = get_amp_computers()

    print(green(f"Fetched AMP4E Computer List"))

    for computer in amp_computer_list:
        if computer["hostname"] == amp_computer_name:
            amp_computer_guid = computer["connector_guid"]

    print(green(f"AMP4E Computer name: {amp_computer_name}, GUID: {amp_computer_guid}"))

    # MISSION03: Complete the AMP query with correct event types to fetch event list
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    amp_query_params = f"connector_guid[]={amp_computer_guid}&MISSIONO3"

    amp_event_list = get_amp_events(query_params=amp_query_params)

    print(green(f"Retrieved {len(amp_event_list)} events from AMP"))

    amp_event = amp_event_list[0]
    
    print (green(f"First Event: {amp_event['event_type']} \
             \nDetection: {amp_event['detection']} \
             \nFile name: {amp_event['file']['file_name']} \
             \nFile sha256: {amp_event['file']['identity']['sha256']}"))

    threatgrid_sha = amp_event["file"]["identity"]["sha256"]

    """
    Step 2. Isolate infected Computer to perform further investigation 
    and make sure that the action was successful.
    """
    
    print(white(f"\nStep 2"))

    amp_computer_isolation = amp_isolation('put',amp_computer_guid)
    
    if amp_computer_isolation:
        print(green(f"Computer {amp_computer_name} (GUID {amp_computer_guid}) is {amp_computer_isolation['status']}"))

    """
    Step 3. In Threat Grid, find all samples, associated with malicious sha256 that you have 
    captured in step 1 and look at analysis report for the first sample on the list.
    """

    print(white(f"\nStep 3"))

    # MISSION05: Use the right function to find all samples, associated with malicious sha256
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    submission_info = MISSION05(threatgrid_sha)

    threatgrid_sample_id = submission_info[0]['item']['sample']

    print(green(f"Successfully retrieved Threat Grid sample ID {threatgrid_sample_id} for sha265 {threatgrid_sha}"))

    """
    Step 4. Request all domains for a specific sample in Threat Grid and store them in an array to get more data out of them.
    """
    print(white(f"\nStep 4"))
    # MISSION07: Pass the right variable to achieve fetch all domains for a specific sample in Threat Grid
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    threatgrid_sample_domains = threatgrid_get_domains(MISSION07)

    print(green(f"Successfully retrieved domains on the sha256 submission: {threatgrid_sample_domains}"))

    """
    Step 5. Check all associated domains against Umbrella Investigate to retrieve their status.
    """
    print(white(f"\nStep 5"))
    # MISSION08: Use the right function and pass the correct variable into it to retrieve the status of the first domain associated with Treat Grid sample.
    # Hint: Remember that numbering starts with 0 in most coding languages.
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    umbrella_domains_status = 'MISSION08'

    umbrella_malicious_domains = []
    
    for domain in threatgrid_sample_domains:
        domain_status = get_umbrella_domain_status(domain)
        if domain_status == 1:
            print(green(f"The domain {domain} is found CLEAN"))
            env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
        elif MISSION10: # MISSION10: Put correct condition with proper domain status value to catch Malicious domains
            print(green(f"The domain {key} is found MALICIOUS"))
            umbrella_malicious_domains.append(domain)
        elif domain_status == 0:
            print(green(f"The domain {key} is found UNDEFINED"))

    """
    Step 6. Using Umbrella Enforcement, post malware events to the API for processing and optionally adding to a customer's domain lists.
    """
    print(white("\nStep 6"))
    
    umbrella_event_id, umbrella_blocklist_enforcement = post_umbrella_events(umbrella_malicious_domains)

    print(green(f"Domains {umbrella_malicious_domains} were accepted, Umbrella event id: {umbrella_event_id}"))

    """
    Step 7. Using Threat Response, inspect if malicious sha256 has been found on our network. 
    Use response capabilities of AMP for Endpoints module to block this malicious file from execution on all Computers in our network.
    """
    print(white("\nStep 7"))

    ctr_access_token = ctr_auth()

    print(green("Received Threat Response access token"))
    
    # MISSION13: Pass free form arbitrary text that contains sha256 obtained in Step 1.
    # Hint: f"suspicious hash is {variable}"
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    ctr_arb_text = MISSION13

    ctr_observables = ctr_inspect(ctr_access_token, ctr_arb_text)

    print(green(f"Received formatted list of observables. Total observables: {len(ctr_observables)}"))

    # MISSION14: Pass to the function properly formatted observables obtained in Step 7.
    # Hint: Check the function and put correct variable there too.
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    ctr_intel = ctr_enrich_observe(ctr_access_token, 'MISSION14')

    print(green(f"Received Sightings"))

    report_time = datetime.now().isoformat()
    ctr_report_path = here / f"ctr_report_{report_time}.json"
    print(blue(f"\n==> Found indicators and sightings. Saving info to: {ctr_report_path}"))
    
    with open(ctr_report_path, "w") as file:
        json.dump(ctr_intel, file, indent=2)

    ctr_enrich_print_scr_report(ctr_intel)
    
    """
    Step 8. Use response capabilities of AMP for Endpoints module in CTR to block this malicious file from execution on all Computers in our network.
    """
    print(white("\nStep 8"))

    # MISSION15: assign function output to correct variable and pass it to function ctr_add_to_amp_scd to perform necessary action.
    # Hint: make sure to pass this variable to the function in validation section too!
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    MISSION15 = ctr_response_actions(ctr_access_token,ctr_observables)

    print(green(f"Received action url for observable: {MISSION15}"))
    env.print_missing_mission_warn(env.get_line()) # Delete this line when mission is complete.
    ctr_action_response = ctr_add_to_amp_scd(ctr_access_token, MISSION15)

    if ctr_action_response == 200:
        print(green(f"A malicious sha256 {threatgrid_sha} is added to AMP Simple Custom Detections list named Quarantine."))

    print(yellow("\nYou are ready for solution validation. Uncomment VALIDATION SECTION in the script. Good luck!"))

    # Step 9. Solution Validation. Uncomment when ready to validate. DO NOT MODIFY THIS SECTION!

    """
    #VALIDATION SECTION START

    print(yellow("\nValidating your solution..."))

    url = f"https://{env.VALIDATOR.get('host')}/python/submit"
    user = get_user_details(webex_token)

    response = post_submission(url, threatgrid_sha, threatgrid_sample_id,
                    threatgrid_sample_domains[0], umbrella_malicious_domains,
                    umbrella_blocklist_enforcement, ctr_observables,
                    ctr_response_url, user["id"])

    if response['message'] == "True":
        print(white("\nCONGRATULATIONS! You have successfully completed the Python mission! "))
    else:
        print(red("\nValidation failed. Please check your solution carefully and try again. Use hints and tips in the lab guide."))
    
    #VALIDATION SECTION END
    """