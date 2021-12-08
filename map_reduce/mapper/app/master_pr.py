from os import name, read
from mapper import get_ips
import os, math
import requests, json


def read_dir(file_path: str) -> list:
    '''
    read number of files present in dir
    '''
    return [name for name in os.listdir(file_path)]

def chunks(l, n):
    """ Yield n successive chunks from bag.
    """
    newn = int(1.0 * len(l) / n + 0.5)
    for i in range(0, n-1):
        yield l[i*newn:i*newn+newn]    
    yield l[n*newn-newn:]

def send_request(file_blobs: list, reducers: list, page_rank_threshold: int, query_type: str)-> bool:
    idx = 0
    for i in chunks(file_blobs, len(reducers)):
        print(i)
        url = f"http://{reducers[idx]}:8080/consume"
        data = {
            'payload':i,
            'page_rank_threshold': page_rank_threshold,
            'query_type': query_type
        }
        headers = {'content-type': 'application/json'}
        try:
            res  = requests.post(url, headers=headers, data=json.dumps(data))
        except Exception as e:
            print(f"Failed to make connection request: {reducers[idx]}, err:{e}")
        if(idx < len(reducers)):
            idx +=1

def main():
    query_type = 'scan'
    # query_type = 'aggregation'
    # file_path = f"../page_rank_data/data_{query_type}"
    # file_path = "../page_rank_data/data_aggre"
    file_path = f"/app/page_rank_data/data_{query_type}"
    pod_ips = get_ips()
    page_rank_threshold = 500
    if(not len(pod_ips)):
        print(f"At least one reducer expected, shutting down: {pod_ips}")
        exit(1)
    
    # pod_ips = ['129.0.0.1', '129.0.0.1', '129.0.0.1']
    number_of_blobs = read_dir(file_path)
    send_request(number_of_blobs, pod_ips, page_rank_threshold, query_type)    



if __name__ == "__main__":
    '''
    - Read number of files from the directory
    - Split the number into available number of reducers
    - Send the reducer file to read along with, the page rank threshold in the body 
    '''
    main()