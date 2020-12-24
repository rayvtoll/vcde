import json, subprocess, os
from flask import Flask, jsonify, request, make_response

externalVolume = "/opt/vcde"
netWork = 'vcd_frontend'

# applications
app = Flask(__name__)
apps = ["gimp", "firefox", "chrome", "libreoffice", "evolution", "geary", "thunderbird", "nautilus"]
appImage = {}
for a in apps:
    appImage[a] = "rayvtoll/vcd-{}:latest".format(a)

class DockerRun:  # class to start application container

    @staticmethod  # docker data of running containers.
    def _data():
        return json.loads(subprocess.check_output('docker network inspect ' + netWork, shell=True))[0]['Containers']
    
    def detect_host(self):  # using _data to retrieve hostname by origin IP of host
        for i in self.data:
            if self.data[i]['IPv4Address'].split("/")[0] == self.ip:
                return self.data[i]['Name']

    def isnew(self):  # check if container excists
        if str(self.host + "-" + self.app) in str(self.data):
            return False
        else:
            return True

    def volumemounts(self): # constructing volumemounts of docker run command
        volumes = ""
        if self.app == "chrome":
            volumes += '--device /dev/dri --security-opt seccomp=/app/chrome.json '

        if self.app == 'firefox' or 'chrome' or 'gimp':
            volumes += '--shm-size=2g '

        volumes += '-v {0}/{1}:/home/{1} -v {0}Public:/home/{1}/Public ' \
                   '-v {0}/{1}/.ssh/id_rsa.pub:/home/{1}/.ssh/authorized_keys:ro' \
                   .format(externalVolume, self.user)
        return volumes

    def dockerstart(self):  # final docker run command
        return "docker run -d --rm --name {0}-{1} --hostname {0}-{1} {2} --network {3} -e USER={4} {5}" \
               .format(self.host, self.app, self.volumemounts, netWork, self.user, appImage[self.app])

    def message(self):  # final response to POST request
        if not self.isnew:
            return "container already running"
        else:
            if not self.availableapp:
                return "application not available"
            else:
                os.system(self.dockerstart)
                return "starting " + self.app

    def __init__(self, app, ip):
        self.app = app
        self.ip = ip
        self.availableapp = self.app in apps
        self.data = DockerRun._data()
        self.host = self.detect_host()
        self.isnew = self.isnew()
        self.user = self.host.split("-")[1]
        self.volumemounts = self.volumemounts()
        self.dockerstart = self.dockerstart()
        self.message = self.message()


@app.route('/', methods=['POST'])
def create_containers():
    requestedApp = request.json.get('app')
    originIP = request.environ['REMOTE_ADDR']
    return jsonify([{"message" : ((DockerRun(requestedApp, originIP)).message)}])

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)