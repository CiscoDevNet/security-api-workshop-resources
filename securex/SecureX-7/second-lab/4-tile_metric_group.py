from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from schemas import DashboardTileDataSchema, DashboardTileSchema
from utils import get_json, get_jwt, jsonify_data
import os
from crayons import *
import requests
import json

def paris_temperature():
    response=requests.get('https://www.prevision-meteo.ch/services/json/lat=46.259lng=5.235')
    payload=response.content
    json_payload=json.loads(payload)
    heures=json_payload['current_condition']['hour'].split(":")
    hour=int(heures[0])
    hour=hour-1
    if hour<0:
        hour=23
    if hour<10:
        hour_str="0"+str(hour)
    else:
        hour_str=str(hour)
    heure=hour_str+':'+heures[1]   
    print(json_payload['current_condition']['date'])
    print(heure)
    print(json_payload['current_condition']['tmp'])
    return (json_payload['current_condition']['date'],heure,json_payload['current_condition']['tmp'])

app = Flask(__name__)

@app.route('/tiles', methods=['POST'])
def tiles():
    try:
        auth = get_jwt()
        return jsonify_data([
        {
            "id": "paris_temperature",
            "type": "metric_group",
            "title": "Real Paris Temperature",
            "periods": ["last_24_hours"],
            "short_description": "Paris Temperature",
            "description": "A longer description",
            "tags": ["test"],
        }         
        ])
    except:
        return jsonify_data([])

@app.route('/tiles/tile', methods=['POST'])
def tile():
    _ = get_jwt()
    _ = get_json(DashboardTileSchema())
    return jsonify_data({})

@app.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    _ = get_jwt()
    req = get_json(DashboardTileDataSchema())
    print (green(req["tile_id"],bold=True))
    if req['tile_id'] == 'paris_temperature':
        date , hour , temp = paris_temperature()
        return jsonify_data(
            {
                "observed_time": {
                    "start_time": "2020-12-19T00:07:00.000Z",
                    "end_time": "2021-01-18T00:07:00.000Z",
                },
                "valid_time": {
                    "start_time": "2021-01-18T00:07:00.000Z",
                    "end_time": "2021-01-18T00:12:00.000Z",
                },
                "data": [
                    {
                        "icon": "brain",
                        "label": "Date",
                        "value": date,
                        "value-unit": "string",
                    },
                    {
                        "icon": "percent",
                        "label": "hour",
                        "value": hour,
                        "value-unit": "string",
                    },
                    {
                        "icon": "percent",
                        "label": "Temperature",
                        "value": temp,
                        "value-unit": "integer",
                    },                    
                ],
                "cache_scope": "org",
            }
        )  

@app.route('/health', methods=['POST'])
def health():   
    data = {'status': 'ok'}
    return jsonify({'data': data}) 

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)