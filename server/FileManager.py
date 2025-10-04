import os
import json
from models import DataQuery

def checkCache(qParams: DataQuery, flag):
    filename = qParams.latitude + '-' + qParams.longetude + ':' + qParams.year
    
    if os.path.isfile("/cache/" + filename + ".json"):
        with open('cache/' + filename + '.json', 'r') as cache:
            data = json.load(cache)
    else:
        #run datascience, make data = return
        data = 1
    
    return data
            
def addCache(qParams: DataQuery, json):
    filename = qParams.latitude + '-' + qParams.longetude + ':' + qParams.year
    
    if os.path.isfile("/cache/" + filename + ".json"):
        return
    
    with open('/cache/' + filename + '.json', 'w') as file:
            file.write(json)
            