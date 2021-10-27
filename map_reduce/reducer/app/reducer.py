from collections import defaultdict
from logging import log
from types import MethodType
from flask import Flask, request
from logger import logging
import time
import json
logger = logging.getLogger('reducer_logger')

app = Flask(__name__)

word_map = {}
def process_data(data):
    for word in data['payload']:
        if word not in word_map:
            word_map[word] = 1
        else:
            word_map[word] = word_map.get(word) +1


def reduce_data(data):
    res = {}
    for k, v in data.items():
        if len(v):
            sum = 0
            for i in v:
                sum +=i
            res[k] = sum
    return res


@app.route("/consume", methods=["POST"])
def consume():
    word_map.clear()
    data = json.loads(request.data)
    logger.debug(f"--- RECEIVED CHUNK-- \n {data}")
    #Process data in sync as the server is async
    process_data(data)
    logger.debug(word_map)
    # logger.debug(f"Printing word map =>, check count for word  \n { word_map['rushi']}") 
    return json.dumps(word_map)

@app.route("/reduce", methods=["POST"])
def reduce():
    data = json.loads(request.data)
    map = {}
    logger.debug(f"--- RECEIVED CHUNK-- \n {data}")
    for chunk in data['payload']:
        map[chunk[0]] = chunk[1]
    #Process data in sync as the server is async
    res =  reduce_data(map)
    return json.dumps(res)

@app.route("/health")
def health():
    return 'Am up X!'

if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)