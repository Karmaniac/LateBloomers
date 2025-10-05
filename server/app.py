from flask import Flask, jsonify, request
from flask_cors import CORS
from models import DataQuery
from FileManager import checkCache

from dotenv import load_dotenv
import os
import json
from utils.utils import authenticate_service_account

app = Flask(__name__)
# swagger = Swagger(app)

CORS(app)

@app.route('/getData', methods=['POST'])
def returnData():
    """Endpoint to get data based on latitude, longitude, and year.
    ---
    post:
      description: Get data based on latitude, longitude, and year.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                latitude:
                  type: number
                  example: 34.0522
                longitude:
                  type: number
                  example: -118.2437
                year:
                  type: integer
                  example: 2023
      responses:
        200:
          description: Data retrieved successfully.
          content:
            application/json:
              schema:
                type: object
        400:
          description: Invalid input.
      
    """
    if request.is_json:
        data = DataQuery.model_validate_json(json.dumps(request.get_json()))
        returnJson = checkCache(data, 0)
        
        return jsonify(returnJson), 200

    return jsonify({"error": "Request must be JSON"}), 400

@app.route('/getDataFollowup')
def returnFollowup():
    """Endpoint to get follow-up data.
    ---
    get:
      description: Get follow-up data.
      responses:
        200:
          description: Follow-up data retrieved successfully.
          content:
            application/json:
              schema:
                type: object
        400:
          description: Invalid input.
    """
    #TODO await the followupdata
    #followup = call full year range
    
    temp = 1 #just for getting rid of errors
    
    #addCache(followup)


@app.route('/test_map', methods=['GET'])
def test_map():
  """Endpoint will retrieve image of earth engine and return mapid and token
  ---
  get:
    description: Retrieve image of earth engine and return mapid and token."""
  mapod = ee.Image('CGIAR/SRTM90_V4').getMapId({'min': 0, 'max': 3000})
  
  template_values = {
    'mapid': mapod['mapid'],
    'token': mapod['token']
  }

  print(template_values)

  return jsonify(template_values), 200


@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    load_dotenv()

    PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH')
    SERVICE_ACCOUNT = os.getenv('SERVICE_ACCOUNT')

    authenticate_service_account(SERVICE_ACCOUNT, PRIVATE_KEY_PATH)
    
    app.run(port=5000, debug=True) # debug=True enables auto-reloading and debugger