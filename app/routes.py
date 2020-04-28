from app import app
from flask import render_template
import concurrent.futures
from app.cisco import Cisco
import yaml

result = {}


@app.route('/')
def index():
    with open('app/hosts.yaml', 'r') as f:
        yml = yaml.load(f)
    devices = list()
    commands = yml['commands']

    for device in yml['devices']:
        devices.append({'params': {
            'host': yml['devices'][device]['ip'],
            'device_type': yml['devices'][device]['device_type'],
            'username': yml['credentials']['login'],
            'password': yml['credentials']['password']},
            'hostname': device}
        )
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        {ex.submit(apply_connect, dev['hostname'], dev['params'], commands): dev for dev in devices}
    return render_template('dashboard.html', devices=result)


def apply_connect(hostname, device, commands):

    c = Cisco(device)
    result[hostname] = {'ip': device['host']}
    result[hostname].update(c.get_cdp())
    result[hostname].update(c.get_ntp())
    result[hostname].update(c.get_version())
    c.set_commands(commands)
    c.save_config(hostname)
    c.close()





