from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from schemas import DashboardTileDataSchema, DashboardTileSchema
from utils import get_json, get_jwt, jsonify_data,current_date_time,date_plus_x_days,epoch_date,epoch_datetime
from sx_get_judgments_demo import donut,update_database,gen_bar_chart_data
import os
from crayons import *
import requests
import json
from datetime import datetime, timedelta
import time

def gen_json_for_bar_chart(data_in,tile_id,key_type):
    temps=current_date_time()
    tile_json={}
    tile_json["valid_time"]={
        "start_time": temps,
        "end_time": temps
    }
    tile_json["tile_id"] = tile_id
    tile_json["keys"] = []
    tile_json["cache_scope"] = "org"
    tile_json["key_type"] = key_type
    tile_json["period"] = "last_7_days"
    tile_json["observed_time"]= {
        "start_time": temps,
        "end_time": temps
    }    
    data_list=[]
    ii=0
    for item in data_in:
        print(cyan(item,bold=True)) 
        print(yellow(len(item),bold=True))
        data_dict_item={}
        data_dict_item["key"]=epoch_date(item[0])        
        url=item[1]
        i=0
        data_dict_item["values"]=[]
        for sub_item in item:
            print(red(i,bold=True))
            entry={}
            if i>1 and i<len(item):
                entry["key"]= item[i]
                entry["value"]= item[i+1]
                entry["tooltip"]= f"{item[i]} : {item[i+1]}"
                entry["link_uri"]= url                             
                data_dict_item["values"].append(entry)
                if ii==0:
                    new_key={}
                    new_key={"key": item[i],"label": item[i]}
                    tile_json["keys"].append(new_key)                
                i+=1
            i+=1            
        data_list.append(data_dict_item)
        ii+=1
    tile_json["data"]=data_list
    return(tile_json)

def gen_json_for_line_chart(data_in,tile_id):
    start_time=current_date_time()
    end_time=current_date_time()    
    tile_json={}
    tile_json["valid_time"]={
        "start_time": start_time,
        "end_time": end_time
    }
    tile_json["tile_id"] = tile_id
    tile_json["keys"] = []
    tile_json["cache_scope"] = "user"
    tile_json["key_type"] = "timestamp"
    tile_json["period"] = "last_7_days"
    tile_json["observed_time"]= {
        "start_time": start_time,
        "end_time": end_time
    }    
    data_list=[]
    ii=0
    for item in data_in:
        print(cyan(item,bold=True)) 
        print(yellow(len(item),bold=True))
        data_dict_item={}
        data_dict_item["key"]=epoch_datetime(item[0])  
        data_dict_item["value"]=item[1]
        data_list.append(data_dict_item)
    tile_json["data"]=data_list
    return(tile_json)
    
def gen_json_for_donut(data_in,tile_id): 
    start_time=current_date_time()
    end_time=current_date_time()    
    tile_json={}
    tile_json["valid_time"]={
        "start_time": start_time,
        "end_time": end_time
    }
    tile_json["tile_id"] = tile_id
    tile_json["labels"] = []
    tile_json["labels"].append([])
    tile_json["labels"].append([])
    tile_json["cache_scope"] = "org"
    tile_json["period"] = "last_7_days"
    tile_json["observed_time"]= {
        "start_time": start_time,
        "end_time": end_time
    }    
    data_list=[]
    ii=0
    key_index=0
    for item in data_in:
        print(cyan(item,bold=True)) 
        print(yellow(len(item),bold=True))
        data_dict_item={}
        data_dict_item["key"]=item[0]   
        data_dict_item["value"]=item[3]
        tile_json["labels"][0].append(item[2])
        url=item[1]
        i=0
        iii=0
        data_dict_item["segments"]=[]
        for sub_item in item:
            print(red(i,bold=True))
            entry={}
            if i>3 and i<len(item):
                entry["key"]= item[i]
                entry["value"]= item[i+1]
                entry["tooltip"]= f"{item[i]} : {item[i+1]}"
                entry["link_uri"]= url                             
                data_dict_item["segments"].append(entry)
                if item[i] not in tile_json["labels"][1]:
                    tile_json["labels"][1].append(item[i])
                if ii==0:
                    new_key={}
                    new_key={"key": iii,"value": item[i]}  
                    iii+=1
                i+=1
            i+=1            
        data_list.append(data_dict_item)
        ii+=1
    tile_json["data"]=data_list
    return(tile_json)

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    gen_bar_chart_data_seven()
    return "DONE"

@app.route('/tiles', methods=['POST'])
def tiles():
    try:
        auth = get_jwt()
        return jsonify_data([
            {
                "title": "HoneyPot Dashboard",
                "description": "Patrick Vertical Histogram",
                "periods": [
                    "last_hour",
                    "last_7_days",
                    "last_30_days"
                ],
                "default_period": "last_7_days",
                "tags": [
                    "pat",
                    "ip_addresses"
                ],
                "type": "vertical_bar_chart",
                "short_description": "The number of bad IP addresses",
                "id": "vertical_histogram"
            },            
            {
                "description": "SecureX IP Blocking List",
                "tags": [
                    "pat"
                ],
                "type": "donut_graph",
                "short_description": "SecureX IP Blocking List",
                "title": "IP Feed Breakdown",
                "default_period": "last_7_days",
                "id": "donut"
            }             
        ])
    except:
        return jsonify_data([])


@app.route('/tiles/tile', methods=['POST'])
def tile():
    _ = get_jwt()
    _ = get_json(DashboardTileSchema())
    return jsonify_data({})
    
@app.route('/tiles/update_database', methods=['GET'])
def update():
    update_database()
    return jsonify_data({})    

@app.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    _ = get_jwt()
    req = get_json(DashboardTileDataSchema())
    print (green(req,bold=True))
    print (green(req["tile_id"],bold=True))
    if req['tile_id'] == 'vertical_histogram':
        if req['period'] == 'last_7_days':
            data=gen_bar_chart_data(7)
        elif req['period'] == 'last_30_days':
            data=gen_bar_chart_data(30)            
        else:
            data=gen_bar_chart_data(1)
        donnees=gen_json_for_bar_chart(data,"vertical_histogram","timestamp")
        #print(cyan(donnees,bold=True))
        return jsonify_data(donnees)
    if req['tile_id'] == 'donut':      
        data=donut()
        info=gen_json_for_donut(data,"donut_tile")
        return jsonify_data(info)        
    elif req['tile_id'] == 'raas':
        return jsonify_data(response_six)    
        
@app.route('/health', methods=['POST'])
def health():   
    update_database()
    data = {'status': 'ok'}
    return jsonify({'data': data}) 

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)