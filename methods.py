import subprocess
import random
import requests

def get_host_info():
    cmd = subprocess.Popen(['hostname', '-a'], stdout=subprocess.PIPE)
    hostname=str(cmd.communicate())[3:].split('\\n')[0]
    cmd = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
    ip_address=str(cmd.communicate())[3:].split('\\n')[0].split()[0]
    return hostname, ip_address

def check_latency(server):
    cmd = "ping -qc3 %s | awk -F'/' 'END{ print $6 }'"%server
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try:
        output = str(ps.communicate()[0])[2:-3] + ' ms'
    except IndexError:
        output = 'No data'
    return output

def speedtest():
    cmd = subprocess.Popen(['speedtest-cli', '--simple', '--secure'], stdout=subprocess.PIPE)
    result = str(cmd.communicate())
    result = result[3:].split('\\n')[:-1]
    return result

def get_home_ping():
    with open('.ping', 'r') as f:
        data = f.read()
    try:
        ping = str(int(data.split()[0])*10 + round(random.uniform(0, 10), 3)) + ' ms'
    except IndexError:
        ping = 'No data'
    return ping

def check_webserver(port=5891):
    response = requests.get(f'http://localhost:{port}/').text
    return response
