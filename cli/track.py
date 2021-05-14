#/usr/bin/python3

from AppKit import NSWorkspace
import json, requests, time, os, sys, subprocess
from datetime import datetime

timer = {}
to_send = {}
base_url = "https://kaalbackend.herokuapp.com/"
root_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(root_dir, "creds.json")

def read_user_data():
    
    with open(credentials_file_path, 'r') as file:
        json_object = json.load(file)
        return json_object

def process():
    entry = 0
    start_time = time.time()
    while True:
        activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
        active = activeAppName
        if entry == 0:
            start_time = time.time()
            entry = 1
            userCred = read_user_data()
            userCred['pid'] = os.getpid();
            file_data = json.dumps(userCred)
            with open(credentials_file_path, 'w') as file:
                file.write(file_data)

        time.sleep(0.1)
        activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
        
        if active != activeAppName:
            entry = 0
            current_time = time.time()
            elapsed_time = "{:.2f}".format(current_time - start_time)
            to_send[activeAppName] = elapsed_time
            # print(to_send)
            payload = {
                "userHash": userCred['userHash'],
                "activities": to_send,
            }

            payload_json = json.dumps(payload)
            response = requests.post("{}/storeactivity/".format(base_url), payload_json)
process()