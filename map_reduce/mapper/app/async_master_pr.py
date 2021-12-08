from os import name, read
from mapper import get_ips
import os, math
import requests, json
import asyncio
from aiohttp import ClientSession

def read_dir(file_path: str) -> list:
    '''
    read number of files present in dir
    '''
    return [name for name in os.listdir(file_path) if os.path.isfile(name)]


def split_per_worker(no_of_files, no_of_reducers):
    '''
    calculate number of files to read per reducer
    '''
    return int(math.ceil(no_of_files/no_of_reducers))

def chunks(l, n):
    """ Yield n successive chunks from bag.
    """
    newn = int(1.0 * len(l) / n + 0.5)
    for i in range(0, n-1):
        yield l[i*newn:i*newn+newn]    
    yield l[n*newn-newn:]

def send_request(file_blobs: list, reducers: list)-> bool:
    idx = 0
    for i in chunks(file_blobs, len(reducers)):
        print(i)
        url = f"http://{reducers[idx]}:8080/consume"
        data = {
            'payload':i
        }
        headers = {'content-type': 'application/json'}
        try:
            res  = requests.post(url, headers=headers, data=json.dumps(data))
        except Exception as e:
            print(f"Failed to make connection request: {reducers[idx]}, err:{e}")
        if(idx < len(reducers)):
            idx +=1

async def create_mapping(pod_ips, bag):
    
    # pod_ips = ['127.0.0.1:8080', '127.0.0.1:4747']
    number_of_mappers = len(pod_ips)    
    idx = 0
    async with ClientSession() as session:
        tasks = []
        for i in chunks(bag, number_of_mappers):
            url = f"http://{pod_ips[idx]}:8080/consume"
            print(f"URL => {url}")        
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

def main():
    file_path = "."
    pod_ips = get_ips()
    if(not len(pod_ips)):
        print(f"At least one reducer expected, shutting down: {pod_ips}")
        exit(1)
    
    # pod_ips = ['129.0.0.1', '129.0.0.1', '129.0.0.1']
    number_of_blobs = read_dir(file_path)
    send_request(number_of_blobs, pod_ips)    



if __name__ == "__main__":
    '''
    - Read number of files from the directory
    - Split the number into available number of reducers
    - Send the reducer file to read along with, the page rank threshold in the body 
    '''
    main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())