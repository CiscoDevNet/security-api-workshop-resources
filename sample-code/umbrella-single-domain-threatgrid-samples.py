import requests
import json

host = "investigate.api.umbrella.com"
api_key = "a0b1c2d3-e4f5-g6h7-i8j9-kalbmcndoepf"
domain = "internetbadguys.com"

print(f"\n==> List Threat Grid samples associated with a domain name")

url = f"https://{host}/samples/{domain}?limit=100&sortby=score"
headers = {'Authorization':'Bearer ' + api_key}

try:
	response = requests.get(url, headers=headers)
except:
	response.raise_for_status()

print (domain)
print (response.json())
