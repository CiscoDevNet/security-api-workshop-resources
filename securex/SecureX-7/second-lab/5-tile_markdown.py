from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from schemas import DashboardTileDataSchema, DashboardTileSchema
from utils import get_json, get_jwt, jsonify_data
import os
from crayons import *

response= {
    "valid_time": {
        "start_time": "2021-04-28T17:06:26.000Z",
        "end_time": "2021-04-28T18:06:26.000Z"
    },
    "tile_id": "markdown_tile",
    "cache_scope": "user",
    "period": "last_hour",
    "observed_time": {
        "start_time": "2021-04-28T17:06:26.000Z",
        "end_time": "2021-04-28T18:06:26.000Z"
    },
    "data": [
        "|   |   |   |",
        "| - | - | - |",
        "| [interface vlan 1](https://www.cisco.com) | ✔ | Up |",
        "| [interface vlan 2](https://www.cisco.com) | ✔ | Up |",
        "| [interface 0/0](https://www.cisco.com) | ✔ | Up |",
        "| [interface 0/1](https://www.cisco.com) | ✖ | Down |",
        "| [interface 0/2](https://www.google.com/) | ✖ | Down |"
    ]
}

app = Flask(__name__)

@app.route('/tiles', methods=['POST'])
def tiles():
    try:
        auth = get_jwt()
        return jsonify_data([
            {
                "description": "A Markdown Tile",
                "periods": [
                    "last_hour"
                ],
                "tags": [
                    "test",
                    "test2"
                ],
                "type": "markdown",
                "short_description": "Shows some markdown stuff",
                "title": "Markdown ASA Interfaces Status",
                "id": "markdown_tile"
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
    if req['tile_id'] == 'markdown_tile':
        return jsonify_data(response)     

@app.route('/health', methods=['POST'])
def health():   
    data = {'status': 'ok'}
    return jsonify({'data': data}) 

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)