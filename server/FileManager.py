import os
import json
from models import DataQuery
from data_import.data_import import fetch_data_year, fetch_data_full

def checkCache(qParams: DataQuery, flag):
    filename = str(qParams.latitude) + '-' + str(qParams.longitude) + ':' + str(qParams.year)
    
    if os.path.isfile("/cache/" + filename + ".json"):
        with open('cache/' + filename + '.json', 'r') as cache:
            data = json.load(cache)
    else:
        #run datascience, make data = return
        data = fetch_data_year(qParams.latitude, qParams.longitude, qParams.year)
    
    return data
            
def addCache(qParams: DataQuery, json):
    filename = qParams.latitude + '-' + qParams.longitude + ':' + qParams.year
    
    if os.path.isfile("/cache/" + filename + ".json"):
        return
    
    with open('/cache/' + filename + '.json', 'w') as file:
            file.write(json)
            