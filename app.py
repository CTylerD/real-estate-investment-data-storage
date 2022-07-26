from flask import (Flask, jsonify, request, abort)
from flask_cors import CORS
import csv
import json
import os

DATA_HEADER_ROW = ["id", "address", "market value", "expenses", "fees", "anticipated ROI"]

def setup_csv():
    """Initializes the csv for storing data entries"""
    if not os.path.exists('investment_app.csv'):
        with open("investment_app.csv", "w", newline="") as csvfile:
            row_writer = csv.writer(csvfile, delimiter=",")
            row_writer.writerow(DATA_HEADER_ROW)


def create_app():
    """Initializes the Flask app"""
    app = Flask(__name__)
    CORS(app)
    setup_csv()
    return app


def get_next_id():
    """Returns the next id in the csv (consecutive integers), to ensure that all entries
       have a unique id. If the csv has no entries yet, sets the first id to 1"""
    with open("investment_app.csv", "r") as csvfile:
        last_line = csvfile.readlines()[-1]
        last_line_list = last_line.split(",")
        if last_line and last_line_list[0] != "id":
            next_id = int(last_line_list[0]) + 1
        else:
            next_id = 1
    return next_id
  

def data_to_json(row):
    """Converts data rows from the csv into json format for returning to the client"""
    output_row = dict()
    for idx, header in enumerate(DATA_HEADER_ROW):
        output_row[header] = row[idx]
    return output_row


app = create_app()

@app.route('/')
def index():
    return abort(404, "the main page is empty - please /add or /retrieve/<id> data")

@app.route('/add', methods=['POST', 'PUT'])
def add_record():
    data = json.loads(request.data.decode('utf-8'))
    try:
        next_id = get_next_id()
        with open("investment_app.csv", "a", newline="") as csvfile:
            row_writer = csv.writer(csvfile, delimiter=",")
            row = [next_id]
            for key in data:
                row.append(data[key])
            row_writer.writerow(row)
        return jsonify({"status": "Entry added successfully!",
                        "entry": data_to_json(row)})
    except Exception:
        return abort(400, "entry unsuccessful, please try again")

@app.route('/retrieve/', methods=['GET'])
def retrieve_record_no_id():
    return abort(400, "no id was specified")

@app.route('/retrieve/<id>', methods=['GET'])
def retrieve_record(id):
    output = dict()
    counter = 1
    with open("investment_app.csv", "r") as csvfile:
        row_reader = csv.reader(csvfile)
        for row in row_reader:
            if row[0] == str(id):
                output = data_to_json(row)
                return jsonify(output)    
        else:
            return abort(404, "An entry with the given key doesn't exist")


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "bad request"
    }), 400


@app.errorhandler(401)
def auth_error_handler(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "not authorized"
    }), 401


@app.errorhandler(403)
def auth_error_handler(error):
    return jsonify({
                    "success": False,
                    "error": 403,
                    "message": "forbidden"
    }), 403


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
                    "success": False,
                    "error": 405,
                    "message": "method not allowed"
    }), 405


@app.errorhandler(409)
def auth_error_handler(error):
    return jsonify({
                    "success": False,
                    "error": 409,
                    "message": "conflict"
    }), 409


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
    }), 422


if __name__ == '__main__':
    app.run()
