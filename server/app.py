from flask import Flask, jsonify, request
from models import DataQuery
from FileManager import checkCache

from dotenv import load_dotenv
import os
import json
from utils.utils import authenticate_service_account

load_dotenv()

PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH')
SERVICE_ACCOUNT = os.getenv('SERVICE_ACCOUNT')

authenticate_service_account(SERVICE_ACCOUNT, PRIVATE_KEY_PATH)

app = Flask(__name__)

@app.route('/getData', methods=['POST'])
def returnData():
    if request.is_json:
        data = DataQuery.model_validate_json(json.dumps(request.get_json()))
        returnJson = checkCache(data, 0)
        
        return jsonify(returnJson), 200

    return jsonify({"error": "Request must be JSON"}), 400

@app.route('/getDataFollowup')
def returnFollowup():
    #TODO await the followupdata
    #followup = call full year range
    
    temp = 1 #just for getting rid of errors
    
    #addCache(followup)

if __name__ == '__main__':
    app.run(debug=True) # debug=True enables auto-reloading and debugger