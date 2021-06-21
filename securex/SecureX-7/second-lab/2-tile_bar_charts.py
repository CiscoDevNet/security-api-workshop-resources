from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from schemas import DashboardTileDataSchema, DashboardTileSchema
from utils import get_json, get_jwt, jsonify_data
import os
from crayons import *
import json

payload_for_bar_charts_h={
    "valid_time": {
        "start_time": "2021-04-27T18:06:26.000Z",
        "end_time": "2021-04-28T18:06:26.000Z"
    },
    "tile_id": "horizontal_histogram_tile",
    "keys": [
        {
            "key": "somethingpat",
            "label": "something label"
        }
    ],
    "cache_scope": "user",
    "key_type": "timestamp",
    "period": "last_24_hours",
    "observed_time": {
        "start_time": "2021-04-27T18:06:26.000Z",
        "end_time": "2021-04-28T18:06:26.000Z"
    },
    "data": [
        {
            "key": "1620597601000",
            "label": "19:00:00",
            "value": 30,
            "values": [
                {
                    "key": "somethingpat",
                    "value": 30,
                    "tooltip": "something: 30",
                    "link_uri": "https://www.google.com"
                }
            ]
        },     
        {
            "key": "1620511201000",
            "label": "19:00:00",
            "value": 10,
            "values": [
                {
                    "key": "somethingpat",
                    "value": 10,
                    "tooltip": "something: 10",
                    "link_uri": "https://www.google.com"
                }
            ]
        },    
        {
            "key": "1620424801000",
            "label": "19:00:00",
            "value": 20,
            "values": [
                {
                    "key": "somethingpat",
                    "value": 20,
                    "tooltip": "something: 20",
                    "link_uri": "https://www.google.com"
                }
            ]
        }
    ]
}

payload_for_bar_charts_v={
    "valid_time": {
        "start_time": "2021-04-27T18:06:26.000Z",
        "end_time": "2021-04-28T18:06:26.000Z"
    },
    "tile_id": "vertical_histogram_tile",
    "keys": [
        {
            "key": "something",
            "label": "something label"
        },
        {
            "key": "somethingelse",
            "label": "somethingelse label"
        },
        {
            "key": "andsomethingelse",
            "label": "andsomethingelse label"
        }        
    ],
    "cache_scope": "user",
    "key_type": "string",
    "period": "last_24_hours",
    "observed_time": {
        "start_time": "2021-04-27T18:06:26.000Z",
        "end_time": "2021-04-28T18:06:26.000Z"
    },
    "data": [
        {
            "key": "FIRST",
            "label": "19:00:00",
            "value": 30,
            "values": [
                {
                    "key": "something",
                    "value": 30,
                    "tooltip": "something: 30",
                    "link_uri": "https://www.google.com"
                },
                {
                    "key": "somethingelse",
                    "value": 50,
                    "tooltip": "somethingelse: 50",
                    "link_uri": "https://www.google.com"
                },
                {
                    "key": "andsomethingelse",
                    "value": 10,
                    "tooltip": "andsomethingelse: 10",
                    "link_uri": "https://www.google.com"
                }  
                
            ]
        },     
        {
            "key": "SECOND",
            "label": "19:00:00",
            "value": 10,
            "values": [
                {
                    "key": "something",
                    "value": 10,
                    "tooltip": "something: 10",
                    "link_uri": "https://www.google.com"
                },                
                {
                    "key": "somethingelse",
                    "value": 50,
                    "tooltip": "somethingelse: 50",
                    "link_uri": "https://www.google.com"
                },
                {
                    "key": "andsomethingelse",
                    "value": 10,
                    "tooltip": "andsomethingelse: 10",
                    "link_uri": "https://www.google.com"
                }  
            ]
        },    
        {
            "key": "THIRD",
            "label": "19:00:00",
            "value": 20,
            "values": [
                {
                    "key": "something",
                    "value": 20,
                    "tooltip": "something: 20",
                    "link_uri": "https://www.google.com"
                },
                {
                    "key": "somethingelse",
                    "value": 50,
                    "tooltip": "somethingelse: 50",
                    "link_uri": "https://www.google.com"
                },
                {
                    "key": "andsomethingelse",
                    "value": 10,
                    "tooltip": "andsomethingelse: 10",
                    "link_uri": "https://www.google.com"
                }  
            ]
        }
    ]
}

app = Flask(__name__)

@app.route('/tiles', methods=['POST'])
def tiles():
    try:
        #auth = get_jwt()
        return jsonify_data([ 
            {
                "title": "Patrick Vertical Histogram",
                "description": "Patrick Vertical Histogram",
                "periods": [
                "last_hour",
                "last_24_hours",
                "last_7_days",
                "last_30_days",
                "last_60_days",
                "last_90_days"
                ],
                "tags": [
                    "tests",
                    "test2"
                ],
                "type": "vertical_bar_chart",
                "short_description": "The number of unique devices communicating on your network",
                "id": "vertical_histogram_tile"
            },
            {
                "title": "Horizontal Bar Chart",
                "description": "Horizontal Bar Chart",
                "periods": [
                "last_hour",
                "last_24_hours",
                "last_7_days",
                "last_30_days",
                "last_60_days",
                "last_90_days"
                ],
                "tags": [
                    "test",
                    "test2"
                ],
                "type": "horizontal_bar_chart",
                "short_description": "The number of unique devices communicating on your network side",
                "id": "horizontal_histogram_tile"
            },            
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
    print (yellow(req["period"],bold=True))
    if req['tile_id'] == 'vertical_histogram_tile':
        return jsonify_data(payload_for_bar_charts_v)
    elif req['tile_id'] == 'horizontal_histogram_tile':
        return jsonify_data(payload_for_bar_charts_h)
    if req['tile_id'] == 'something_else':
        return jsonify_data(payload_for_bar_charts)         

@app.route('/health', methods=['POST'])
def health():   
    data = {'status': 'ok'}
    return jsonify({'data': data}) 

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)