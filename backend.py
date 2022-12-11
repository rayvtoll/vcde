# Using -v for the moment
externalVolume = '/tmp/vcde'

# Other variables
netWork = 'vcd_frontend'
vcdImage = 'rayvtoll/containerdesktop:latest'
timeZone = 'TZ="Europe/Amsterdam"'

import os
import subprocess
from flask import Flask, jsonify, request, make_response
import json
app = Flask(__name__)

# endpoint for login container to check what containers are currently running
@app.route('/', methods=['GET'])
def list_containers():
    dockerPs = 'docker ps --format "{{ json .}}" | jq --slurp .'
    return subprocess.check_output(dockerPs, shell=True)

# endpoint for creating new desktopcontainer
@app.route('/', methods=['POST'])
def create_container():
    dockerRun = 'docker run --rm -e {0} -h vcd-{1} --name vcd-{1} -d --network {2} -e USER={1} -v {3}/{1}/:/home/{1}/ '\
                '-v {3}/Public:/home/{1}/Public {4}'.format(timeZone, request.json, netWork, externalVolume, vcdImage)
    return jsonify([{'request' : dockerRun }, {'exitcode' : os.system(dockerRun)}])

# error handling
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

# let's get going
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)