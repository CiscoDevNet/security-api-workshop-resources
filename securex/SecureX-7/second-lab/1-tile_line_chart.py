from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from schemas import DashboardTileDataSchema, DashboardTileSchema
from utils import get_json, get_jwt, jsonify_data
import os
from crayons import *
import json

payload_for_line_chart={
                "observed_time": {
                    "start_time": "2020-12-28T04:33:00.000Z",
                    "end_time": "2021-01-27T04:33:00.000Z",
                },
                "valid_time": {
                    "start_time": "2021-01-27T04:33:00.000Z",
                    "end_time": "2021-01-27T04:38:00.000Z",
                },
                "key_type": "timestamp",
                "data": [
                    {"key": 1611731572, "value": 13},
                    {"key": 1611645172, "value": 20},
                    {"key": 1611558772, "value": 5},
                    {"key": 1611431572, "value": 13},
                    {"key": 1611345172, "value": 20},
                    {"key": 1611258772, "value": 5},
                    {"key": 1611131572, "value": 13},
                    {"key": 1611045172, "value": 20},
                    {"key": 1610958772, "value": 5},
                    {"key": 1610831572, "value": 13},
                    {"key": 1610745172, "value": 20},
                    {"key": 1610658772, "value": 5},
                    {"key": 1610531572, "value": 13},
                    {"key": 1610445172, "value": 20},
                    {"key": 1610358772, "value": 5},
                ],
                "cache_scope": "org",
            }

app = Flask(__name__)

@app.route('/tiles', methods=['POST'])
def tiles():
    try:
        #auth = get_jwt()
        return jsonify_data([
            {
                "id": "test-line-chart-graph",
                "type": "line_chart",
                "title": "Test Graph",
                 "periods": [
                "last_hour",
                "last_24_hours",
                "last_7_days",
                "last_30_days",
                "last_60_days",
                "last_90_days"
                ],
                "short_description": "A short description",
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
    if req['tile_id'] == 'test-line-chart-graph':
        return jsonify_data(payload_for_line_chart) 
    if req['tile_id'] == 'something_else':
        return jsonify_data(response2)         

@app.route('/health', methods=['POST'])
def health():   
    data = {'status': 'ok'}
    return jsonify({'data': data}) 

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)