###############################################################################
# Dependencies
###############################################################################

# This is the flask module, a lightweight server tool
# Flask itself is often used for bootstrapping API services
from flask import Flask, request, send_from_directory, make_response
# Some basic python dependencies below
import sys
import json
import pprint
import os
# Requests allows you to make requests to other APIs from your flask program
import requests

###############################################################################
# App initialization
###############################################################################

app = Flask(__name__, static_url_path='/', static_folder='')

# Here's an example of having local config variables
# In this case, we are loading in the "RUNNING_ENVIRONMENT" variable from our
#   environment. When testing on our machine, we might say 
#   "export RUNNING_ENVIRONMENT=development", and on live we would make that
#   production instead.
# RUNNING_ENVIRONMENT = os.getenv('RUNNING_ENVIRONMENT').strip()
api_key = os.getenv('WEATHER_API_KEY').strip()

###############################################################################
# Resource access definitions
###############################################################################

# The default route of our website - send a static index.html page
# You don't actually need this unless you plan on showing your data from
#   a live webpage.
@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('static/index.html')

# Easy way to allow JavaScript files from a certain directory
@app.route('/js/<path:path>', methods=['GET'])
def send_js(path):
    return send_from_directory('js', path)

# Easy way to allow CSS files from a certain directory
@app.route('/css/<path:path>', methods=['GET'])
def send_css(path):
    return send_from_directory('css', path)


###############################################################################
# Data management definitions
###############################################################################

# The public facing route for getting raw data
# This is useful for loading the data into your main page using AJAX requests
@app.route('/api-test', methods=['GET'])
def check_data():
    data = None
    try:
        data = fetch_data()
        data = preprocess_data(data)
    except():
        return make_response(json.dumps({'error': 'An error occurred'}), 404, {'ContentType': 'application/json'})
    return make_response(json.dumps({'data': data}), 200, {'ContentType': 'application/json'})

###############################################################################
# API access and parsing
###############################################################################

# Let's fetch data
def fetch_data():
    # Your URL
    url_to_get = "http://api.wunderground.com/api/" + api_key + "/geolookup/conditions/q/MA/Boston.json"
    print url_to_get
    print 'Making a request'
    # The following line initiates a request from Flask to your chosen API
    # This code executes synchronously, so no need to get flashbacks to
    #   JavaScript callback hell
    response = requests.get(url_to_get)
    print response

    # We successfully retrieved data
    if (response.ok):
        return json.loads(response.text)
    else:
        assert False
        return None

# Some preprocessing before you send your data to other interfaces
# Convert timezones, remove tokens, etc.
def preprocess_data(data):
    return data

# This is a simple function to dump your data to a CSV file for viewing in
#   another program, like Excel. This works for data that is structured
#   as an array of "objects", e.g. [{data1}, {data2}, {data3}].
#   Ultimately you should figure out how to structure this function for your
#   own data needs.
def write_to_csv(data):
    with open('post_data.csv', 'w') as f:
        print data[0]
        dw = csv.DictWriter(f, data[0].keys())
        dw.writeheader()
        for d in data:
            for field in d:
                if isinstance(d[field], basestring):
                    d[field] = d[field].encode('utf-8')
                else:
                    d[field] = str(d[field])
            dw.writerow(d)




###############################################################################
# Misc.
###############################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
