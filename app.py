import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

Stocks = {}

#global variables
currentID = 1


def genID():
    return currentID+1

@app.route('/stocks', methods=['POST'])

def addStock():
    print('POST stock')
    try:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify({'error':'Expected application/json media type'}), 415
        data = request.get_json()
        # Check for required fields in object
        required_fields =['symbol','purchase price','shares']
        if not all(field in data for field in required_fields):
            return jsonify({'error':'Malformed Data'}), 400
        newID=genID()
        if 'name' not in data:
            name = "NA"
        else:
            name = data['name']
        if 'purchase date' not in data:
            purchase_date = "NA"
        else:
            purchase_date = data['purchase date']
        stock = {
            'id' : newID,
            'symbol' : data['symbol'],
            'purchase price' :  data['purchase price'],
            'shares' : data['shares'],
            'name' : name,
            'purchase date' : purchase_date           
        }

        Stocks[newID] = stock
        response_data = {"id":newID}
        return jsonify(response_data), 201

    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"server error":str(e)}), 500
    
@app.route('/stocks/{id}', methods=['GET'])

def getIDStock():
    try:
        response_data = Stocks[{id}]
        if response_data is None :
            return jsonify({"error: Stock not found"}), 404 
        return jsonify(response_data), 200
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"server error":str(e)}), 500 
    
@app.route('/stocks/{id}', methods=['DELETE'])

def deleteStock():
    try:
        if Stocks[{id}] is None:
            return jsonify({"error: Stock not found"}), 404 
        else:
            Stocks[{id}] = None
            return jsonify(''), 204
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"server error":str(e)}), 500
    
@app.route('/stocks/{id}', methods=['PUT'])

def updateStock():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify({'error':'Expected application/json media type'}), 415
        data = request.get_json()
        required_fields =['id', 'symbol','purchase price','shares','name', 'purchase date']
        if not all(field in data for field in required_fields):
            return jsonify({'error':'Malformed Data'}), 400
        if Stocks[{id}] is None:
            return jsonify({"error: Stock not found"}), 404 
        Stocks[{id}] = data #very nice!
        return jsonify({"id":{id}}),200
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"server error":str(e)}), 500
    
@app.route('/stock-value/{id}', methods=['GET'])

def getStockValue():
    try:
        if Stocks[{id}] is None:
            return jsonify({"error: Stock not found"}), 404 
        data = Stocks[{id}]
        symbol = data['symbol']
        api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
        response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
        if response.status_code == requests.codes.ok:
            ticker = response.text    
        else:
            print("Error:", response.status_code, response.text)

        #api_url_value = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
        #if response.status_code == requests.codes.ok:
            #stockValue = response.text    
        #else:
            #print("Error:", response.status_code, response.text)


    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"server error":str(e)}), 500