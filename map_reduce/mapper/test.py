import socket
import os
import time
pod_ips = set()
def get_ips():
    svc_name = os.getenv("MAP_REDUCE_SVC")
    print("---------------------")
    print(svc_name)
    pod_eps = socket.getaddrinfo(svc_name,0,socket.AF_INET,socket.SOCK_DGRAM)
    print(pod_ips)
    for ip in pod_eps:
        print(ip)
        print(type(ip))
        
        pod_ips.add(ip[-1])

def chunks(l, n):
    """ Yield n successive chunks from bag.
    """
    newn = int(1.0 * len(l) / n + 0.5)
    for i in range(0, n-1):
        yield l[i*newn:i*newn+newn]    
    yield l[n*newn-newn:]



if __name__ == "__main__":
    # get_ips()
    l = range(233)
    three_chunks = chunks (l, 4)
    for chunk in chunks(l,4):
        print(chunk)
    # print(three_chunks.next())
    # print(three_chunks.next())
    # print(three_chunks.next())
    # print(three_chunks.next())
    # print(three_chunks.next())