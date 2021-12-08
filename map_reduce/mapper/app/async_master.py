from mapper import get_ips
import os 
import requests
import json
from logger import logging
import asyncio
from aiohttp import ClientSession
from collections import defaultdict


logger = logging.getLogger('mapper_logger')


path_of_file = "Latin-Lipsum.txt"

def split_file():
    #create bag of words from file
    bag = []
    with open(path_of_file, "r") as file:
        for line in file.readlines():
            for word in line.split():
                bag.append(word)
    return bag

def chunks(l, n):
    """ Yield n successive chunks from bag.
    """
    newn = int(1.0 * len(l) / n + 0.5)
    for i in range(0, n-1):
        yield l[i*newn:i*newn+newn]    
    yield l[n*newn-newn:]



async def make_requests(session, url,  data, ip):
    headers = {'content-type': 'application/json'}
    response = await session.post(url, headers=headers, data=json.dumps(data))
    return { 'IP': ip,  'Object': response }


# Testing async master
global_map = defaultdict(list)

async def create_mapping(pod_ips, bag):
    
    # pod_ips = ['127.0.0.1:8080', '127.0.0.1:4747']
    logger.debug("--***----")
    logger.debug(f"Pod Ips =>> {pod_ips}")
    logger.debug("------")
    number_of_mappers = len(pod_ips)    
    idx = 0
    async with ClientSession() as session:
        tasks = []
        for i in chunks(bag, number_of_mappers):
            url = f"http://{pod_ips[idx]}:8080/consume"
            logger.debug(f"URL => {url}")        
            data = {
                'payload':i
            }
            task = asyncio.create_task(make_requests(session, url, data, pod_ips[idx]))
            tasks.append(task)
            if(idx < len(pod_ips)):
                idx +=1
        responses = await asyncio.gather(*tasks)
        for res in responses:
            response = res['Object']
            data = json.loads( await response.read())
            for word in data:
                global_map[word].append(data[word])

async def reduce(data, pod_ips):
    number_of_reducers = len(pod_ips)
    idx = 0
    async with ClientSession() as session:
        tasks = []
        for i in chunks(data, number_of_reducers):
            url = f"http://{pod_ips[idx]}:8080/reduce"
            logger.debug(f"URL => {url}")        
            data = {
                'payload':i
            }
            task = asyncio.create_task(make_requests(session, url, data, pod_ips[idx]))
            tasks.append(task)
            if(idx < len(pod_ips)):
                idx +=1
        responses = await asyncio.gather(*tasks)
        final_reduced = {}
        for res in responses:
            response = res['Object']
            data = json.loads( await response.read())
            final_reduced[res['IP']] = data

        return final_reduced

def convert_map_list(data):
    word_list = []
    for k,v in data.items():
        word_list.append([k, v])
    
    return word_list

async def main():
    '''
    - Split file
    - bag of words / number of mappers
    - Assign workload to each mapper
    - Get the work <- workers will give back number of words it have
    - club the maps [Shuffle step], add number of word recevied
        from reducer
            {
                'hello': [3, 1, 2]
            }
    - give structure back to reducer it will combine the tasks 
            {
                'hello' : 6
            }
    '''
    pod_ips = get_ips()
    bag = split_file()
    task = asyncio.create_task(create_mapping(pod_ips, bag))
    await asyncio.gather(task)
    # print('not waiting')
    map_to_list = convert_map_list(global_map)
    print(len(map_to_list))

    reduce_task = asyncio.create_task(reduce(map_to_list, pod_ips))
    result  = await asyncio.gather(reduce_task)
    print("---- RESULT ---", path_of_file)
    # print(result)
    
    

if __name__ == "__main__":
    main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())