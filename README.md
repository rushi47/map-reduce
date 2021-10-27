# map-reduce
Trying to implement Map-Reduce on k8s

Rough doc to use the repo :-
* Install charts from k8s-charts folder

  `helm install -n map map k8_chars --create-namespace`
  
* Should spin two masters and 4 worker replicas

* Master lifts the load of splitting workload into available number of reducers, while workers perform the reduce operation

* Workers run with Headless service, so ip of workers are fetch from master by dns lookup

* Log in, in one of the masters
  `kubectl exec -it map-xyxyxy bash -n map`

* And run `python async_master.py` 

* Above command will read text from Lorem ipsum. Create bag of word and give it to workers to calculate the number of
words present. Once response is collected, master will do shuffle operation & give back the data again to workers for
reduce operation.
