import json
from flask import Flask, request
import json, os
import resource

app = Flask(__name__)



map = {}
# 30 MB can store => 10,000 so 1/MB it will be 333 records now assuming
# 1 gib of RAM which 1000MB net net we can store 333, 000 records and after that we 
# can clear the map and write it in file
map_counter = 333000
# map_counter = 10


def write_map_file(out_file):
    global map_counter
    for url, val in map.items():
        tmp = f"{url}, {val}\n"
        out_file.write(tmp)  
    #clear the map, and set again counter to 0
    map.clear()  
    map_counter = 0

def process_scan(line, page_rank_threshold, out_file):
    parts = line.split(",")
    try:
        url, page_score = parts[0], int(parts[1])
        if page_score > page_rank_threshold:
            tmp = f"{url}, {page_score} \n"
            out_file.write(tmp)
    except Exception as e:
        pass
        # print("Iseeueee :::", line)

def process_agre(line, page_rank_threshold, out_file):
    global map_counter
    '''
    - to aggregate we need to lookup if the current element was seen.
    - now if we need to check if current element was always seen we can use hashmap
    - this is bad cause it will blow out in memory, instead we create hash function which 
    always gives same number when passed same string and we write on that number which will be our line number
     in FILE
    '''
    parts = line.split(",")
    try:
        ip, rev = parts[0], float(parts[3])
        
        if ip not in map:
            map[ip] = rev
        else:
            map[ip] += rev
        if(map_counter >= 0):
            map_counter -= 1
        else:
            write_map_file(out_file)
        # tmp = f"{ip}, {rev} \n"
        # print(tmp)
        # out_file.write(tmp)
    except Exception as e:
        print(f"Some error : {e}, line : {line}")
        pass 

def process_data(line, page_rank_threshold, out_file, query_type):
    if query_type == 'scan':
        process_scan(line, page_rank_threshold, out_file)
    else:
        process_agre(line, page_rank_threshold, out_file)
        # print("Iseeueee :::", line)

def read_in_chunks(file_object, chunk_size=4024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def perform_external_read(list_of_files, page_rank_threshold, query_type):
    # base_path = f"../../mapper/page_rank_data/data_{query_type}"
    base_path = f"/app/page_rank_data/data_{query_type}"
    op_file = os.path.join(base_path, f"output_file_query_{query_type}")
    #remove existing file if exists
    if os.path.exists(op_file): os.remove(op_file)
    with open(op_file, 'a+') as out_file:
        for file in list_of_files:
            file_path = os.path.join(base_path, file)
            with open(file_path) as f:
                if 'output' not in file:
                    for line in f: #by default iterator is lazy in this case doesnt read in memory
                        process_data(line, page_rank_threshold, out_file, query_type)
                # if line is not split into newlines use below generator: https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
                # for line in read_in_chunks(f):
                #     process_data(line, page_rank_threshold)
        if len(map):
            write_map_file(out_file)
    
@app.route("/consume", methods=["POST"])
def consume():
    data = json.loads(request.data)
    # print(data)
    #https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
    print("*************************")
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print("*************************")
    perform_external_read(data['payload'], data['page_rank_threshold'], data['query_type'])
    print("*************************")
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print("*************************")
    print("Length of map : ", len(map))
    return 'Receieved', 200

@app.route("/health")
def health():
    return 'Am up X!'

if __name__ == "__main__":
    '''
    - receive the name of file to read 
    - load part by part of file in memory and check the number of file above threshold
    - write lines with values more than threshold in op file
    '''
    app.run("0.0.0.0", port=8080, debug=True)