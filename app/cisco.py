from netmiko import ConnectHandler
import re
import textfsm
import os
import time


class Cisco:
    _net = None

    def __init__(self, device):
        self._net = ConnectHandler(**device)

    def get_cdp(self):
        cdp_output = self._net.send_command('show cdp neighbors detail')
        if re.search('cdp is not enabled', cdp_output, re.IGNORECASE):
            return {'cdp_active': False}

        with open('app/output_templates/cdp.txt') as template:
            fsm = textfsm.TextFSM(template)
            result = fsm.ParseText(cdp_output)
            return {'cdp': result, 'cdp_active': True}

    def get_version(self):
        version_out = self._net.send_command('show ver')
        npe_or_not = 'PE'
        if 'NPE' in version_out:
            npe_or_not = 'NPE'
        match = re.match('^.+,\s(\w+)\s.+version\s(.+),', version_out.split('\n')[1], re.IGNORECASE)
        model = match.group(1)
        version = match.group(2)
        return {'model': model, 'version': version, 'npe': npe_or_not}

    def get_ntp(self):
        ntp_out = self._net.send_command('sh ntp status')
        if 'synchronized' in ntp_out:
            return {'ntp': True}
        return {'ntp': False}

    def set_commands(self, commands):
        self._net.send_config_set(commands)

    def save_config(self, hostname):
        output = self._net.send_command('sh run')
        if os.path.exists('backup_config') is False:
            os.mkdir('backup_config')
        datetime = time.strftime('%Y_%m_%d_%H:%M:%S')
        file_name = hostname + '_' + datetime
        with open(f'backup_config/{file_name}', 'w') as f:
            f.write(output)

    def close(self):
        self._net.disconnect()
