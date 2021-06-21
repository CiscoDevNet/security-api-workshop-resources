from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from schemas import DashboardTileDataSchema, DashboardTileSchema
from utils import get_json, get_jwt, jsonify_data
import os
from crayons import *

response_two = {
    "labels": [
        [
            "Open",
            "New",
            "Closed"
        ],
        [
            "Assigned",
            "Unassigned"
        ]
    ],
    "valid_time": {
        "start_time": "2021-04-28T16:48:18.000Z",
        "end_time": "2021-04-28T17:48:18.000Z"
    },
    "tile_id": "donut_tile",
    "cache_scope": "user",
    "period": "last_hour",
    "observed_time": {
        "start_time": "2021-04-28T16:48:18.000Z",
        "end_time": "2021-04-28T17:48:18.000Z"
    },
    "data": [
        {
            "key": 0,
            "value": 2,
            "segments": [
                {
                    "key": 0,
                    "value": 10
                },
                {
                    "key": 1,
                    "value": 20
                }
            ]
        },
        {
            "key": 1,
            "value": 10,
            "segments": [
                {
                    "key": 0,
                    "value": 8
                },
                {
                    "key": 1,
                    "value": 0
                }
            ]
        },
        {
            "key": 2,
            "value": 5,
            "segments": [
                {
                    "key": 0,
                    "value": 0
                },
                {
                    "key": 1,
                    "value": 0
                }
            ]
        }
    ]
}

app = Flask(__name__)

@app.route('/tiles', methods=['POST'])
def tiles():
    try:
        auth = get_jwt()
        return jsonify_data([
        {
                "description": "DONUTS",
                "periods": [
                    "last_24_hours",
                    "last_7_days",
                    "last_30_days",
                    "last_60_days",
                    "last_90_days"
                ],
                "tags": [
                    "AWS"
                ],
                "type": "donut_graph",
                "short_description": "DONUTS",
                "title": "Patrick DONUT",
                "default_period": "last_7_days",
                "id": "donut_tile"
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
    if req['tile_id'] == 'donut_tile':
        return jsonify_data(response_two)

@app.route('/health', methods=['POST'])
def health():   
    data = {'status': 'ok'}
    return jsonify({'data': data}) 

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)