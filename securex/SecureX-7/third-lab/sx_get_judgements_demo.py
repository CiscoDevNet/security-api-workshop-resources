'''
 Get all judgements in your private intelligence, put all result into tinyDB
 with json output and csv output
 
 resource for honeypot_tiles_demo.py
'''
import requests
import json
from crayons import *
import sys
import datetime
import sqlite3

def insert_data_to_db(data):
    sql_create="CREATE TABLE IF NOT EXISTS judgements ( id text PRIMARY KEY, observable text, date text, time text,source text, disposition text, disposition_name text);"
    sql_add="INSERT OR REPLACE into judgements (id, observable, date, time,source, disposition, disposition_name) VALUES (?,?,?,?,?,?,?);"    
    #with sqlite3.connect(:memory:) as conn:
    with sqlite3.connect('database.db') as conn:
        c=conn.cursor()
        try:
            c.execute(sql_create)
        except:
            sys.exit("couldn't create database")
        try:
            c.executemany(sql_add, data)
        except:
            sys.exit("Error adding data to db")
        return(c)
    return()

def read_db(database,operator,filter):
    liste=[]
    with sqlite3.connect(database) as conn:
    #with sqlite3.connect(:memory:) as conn:
        cursor=conn.cursor()
        sql_request = "SELECT * from judgements"
        try:
            cursor.execute(sql_request)
            for resultat in cursor:
                #print(resultat)        
                liste.append(resultat)
        except:
            sys.exit("couldn't read database")
    return(liste)


def get_judgments():    
    with open('data.json') as file:
        data=file.read()        
    items=json.loads(data)  
    list_result=[]
    ii=0
    for item in items: 
        #print(yellow(item,bold=True))
        #print(red(ip,bold=True))            
        datetime=item['timestamp'].split('T')
        the_time=datetime[1][:-4] 
        list_result.append((ii, item['observable']['value'], datetime[0], the_time,item['source'],str(item['disposition']), item['disposition_name']))   
        ii+=1
    return (list_result)

def gen_donut_data():
    liste=[]
    with sqlite3.connect('database.db') as conn:
        cursor=conn.cursor()        
        try:
            sql_request = "SELECT count(*) as nb from judgements where source = 'Patrick HoneyPot'"
            cursor.execute(sql_request)
            nb1=cursor.fetchone()[0]
            print(cyan(nb1))
            sql_request = "SELECT count(*) as nb from judgements where source = 'check.torproject.org'"
            cursor.execute(sql_request)
            nb2=cursor.fetchone()[0]
            print(cyan(nb2))            
        except:
            sys.exit("database access error")
    data=[
[
    "0",
    "http://localhost:4000/tiles/update_database",
	"Patrick HoneyPot",nb1
],
[
	"1",
    "http://localhost:4000/tiles/update_database",
	"check.torproject.org",nb2   
]
]        
    return(data)    
    
def gen_bar_chart_data(days):    
    liste=[]
    with sqlite3.connect('database.db') as conn:
        cursor=conn.cursor()        
        sql_request = "SELECT *,count(*) from judgements where source = 'Patrick HoneyPot' and disposition_name = 'Suspicious' group by `date`"
        cursor.execute(sql_request)
        rows = cursor.fetchall()
        nombre=len(rows)
        nombre0=int(nombre-days)
        print(nombre)
        data=[]
        dict_items={}
        for i in range(0,days):
            #print(cyan(rows[nombre0+i]))
            line=f"{rows[nombre0+i][2]} : {rows[nombre0+i][7]}"
            dict_items[rows[nombre0+i][2]]=rows[nombre0+i][7]
            print(cyan(line)) 
        sql_request = "SELECT *,count(*) from judgements where source = 'Patrick HoneyPot' and disposition_name = 'Malicious' group by `date`"
        cursor.execute(sql_request)
        rows = cursor.fetchall()
        nombre=len(rows)
        nombre0=int(nombre-days)
        print(nombre)        
        for i in range(0,days):
            list_items=[]
            if rows[nombre0+i][2] not in dict_items:
                suspicious_nb='0'
            else:
                suspicious_nb=dict_items[rows[nombre0+i][2]]
            print(cyan(rows[nombre0+i]))
            print(red(suspicious_nb))            
            url=f"http://localhost:6060/focus/focus.php?date={rows[nombre0+i][2]}"
            line=f"{rows[nombre0+i][2]}, {suspicious_nb} , {rows[nombre0+i][7]}"
            list_items.append(rows[nombre0+i][2])
            list_items.append(url)
            list_items.append("suspicious")
            list_items.append(suspicious_nb)
            list_items.append("malicious")
            list_items.append(rows[nombre0+i][7])
            #print(cyan(list_items))
            data.append(list_items)
    print(cyan(data))
    return(data)      

def update_database():    
    start_time = datetime.datetime.now() 
    print(yellow('Get All judgements from SecureX',bold=True))
    judgments=get_judgments()
    print(green(judgments,bold=True))
    print(green(' -> OK DONE',bold=True))
    print(yellow('insert data into sqliteDB',bold=True))
    cursor=insert_data_to_db(judgments)    
    print(green(' -> OK DONE',bold=True))
    return()

def donut():    
    print(yellow('generate donut data',bold=True))
    patrick_honeypot,tor=gen_donut_data()
    print(cyan(f'patrick_honeypots :{patrick_honeypot}',bold=True))
    print(cyan(f'tor :{tor}',bold=True))
    print(green(' -> OK DONE',bold=True))
    print(green('ALL DONE',bold=True))
    return(patrick_honeypot,tor)

def main():  
    start_time = datetime.datetime.now()
    print(yellow('Get Access Token',bold=True))
    access_token=get_token(client_id,client_password)
    #print(green(access_token,bold=True))  
    print(green(' -> OK DONE',bold=True))    
    print(yellow('Get All judgements from SecureX',bold=True))
    judgments=get_judgments()
    #print(green(judgments,bold=True))
    print(green(' -> OK DONE',bold=True))
    print(yellow('insert data into sqliteDB',bold=True))
    cursor=insert_data_to_db(judgments)    
    print(green(' -> OK DONE',bold=True))
    '''
    #print out database content
    resultats = read_db("database.db",'=','80')    
    if resultats :
        for resultat in resultats:
            print(resultat)
    else:
        print('NO RESULTS')
    '''
    print(yellow('generate donut data',bold=True))
    suspicious,malicious=gen_donut_data()
    print(cyan(f'suspicious :{suspicious}',bold=True))
    print(cyan(f'malicious :{malicious}',bold=True))
    print(green(' -> OK DONE',bold=True))
    cursor.close()
    print(green('ALL DONE',bold=True))  
    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = int(time_diff.total_seconds() * 1000)
    execution_time = str(execution_time)+' msec '
    print(execution_time)
if __name__ == "__main__":
    #main()
    gen_bar_chart_data_seven()
