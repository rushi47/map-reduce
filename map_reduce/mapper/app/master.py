from mapper import get_ips
import os 
import requests
import json
from logger import logging


logger = logging.getLogger('mapper_logger')


bag = []
def split_file():
    #create bag of words from file
    path_of_file = "Latin-Lipsum.txt"
    with open(path_of_file, "r") as file:
        for line in file.readlines():
            for word in line.split():
                bag.append(word)


def chunks(l, n):
    """ Yield n successive chunks from bag.
    """
    newn = int(1.0 * len(l) / n + 0.5)
    for i in range(0, n-1):
        yield l[i*newn:i*newn+newn]    
    yield l[n*newn-newn:]

def get_reducers():
    split_file()
    pod_ips = get_ips()
    logger.debug("--***----")
    logger.debug(f"Pod Ips =>> {pod_ips}")
    logger.debug("------")
    number_of_mappers = len(pod_ips)    
    idx = 0
    for i in chunks(bag, number_of_mappers):
        logger.debug("-------IPS---------")
        logger.debug(pod_ips[idx])
        url = f"http://{pod_ips[idx]}:8080/consume"
        logger.debug(f"URL => {url}")        
        data = {
            'payload':i
        }
        headers = {'content-type': 'application/json'}
        res  = requests.post(url, headers=headers, data=json.dumps(data))
        logger.debug(res)
        idx +=1


def main():
    '''
    - Split file
    - bag of words / number of mappers
    - Assign workload to each mapper
    '''
    get_reducers()

if __name__ == "__main__":
    main()