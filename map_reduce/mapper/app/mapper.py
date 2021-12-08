import re
import requests
from flask import Flask
import socket
import threading
import os
import json
import time

app = Flask(__name__)



def get_ips():
    pod_ips = []
    svc_name = os.getenv("MAP_REDUCE_SVC")
    print(f"Service name from env - {svc_name}")
    pod_eps = socket.getaddrinfo(svc_name,0,socket.AF_INET,socket.SOCK_DGRAM)
    for ip in pod_eps:            
        # print(f"Pod ips -   {ip[-1][0]}")
        pod_ips.append(ip[-1][0])
    return pod_ips

@app.route("/get_data")
def get_data():
    return 'working'

@app.route("/health")
def health():
    return 'Am up X!'

@app.route("/get_pod_ips")
def list_eps():
    get_ips()
    return json.dumps(str(get_ips()))

if __name__ == "__main__":
    '''
    - read the data from file
    - split the file into bag of words
    - compute number of reducers
    - split the bag of words between this reducers
    '''
    app.run("0.0.0.0", 8080, debug=True)