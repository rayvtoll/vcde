#python3

# import variables
import os, subprocess, time, json, logging

dockerPs = 'docker ps --format "{{ json .}}" | jq --slurp .'

def vacuumC(data):
    for i in range(0, len(data)):
        if data[i]['Names'].startswith('vcd-'):
            if "seconds" not in data[i]['RunningFor']:
                # check for application containers
                if data[i]['Names'].count('-') > 1:
                    activeSSHString = 'docker exec {} ps aux | egrep "[s]shd: "'.format(data[i]['Names'])
                    if os.system(activeSSHString):
                        logging.warning("deleting: {}".format(data[i]['Names']))
                        os.system("docker container rm -f {}".format(data[i]['Names']))

                # check for desktop containers
                else:
                    activeSessionString = "docker exec {} ps -ef h | grep xrdp".format(data[i]['Names'])
                    activeSession = subprocess.check_output(activeSessionString, shell=True)
                    if not "Xorg" in str(activeSession):
                        logging.warning("deleting: {}".format(data[i]['Names']))
                        os.system("docker container rm -f {}".format(data[i]['Names']))


# Vacuum cleaner for closed application and desktop containers 
while True:
    time.sleep(30)
    X = subprocess.check_output(dockerPs, shell=True).decode('utf-8')
    data = json.loads(str(X))
    vacuumC(data)
