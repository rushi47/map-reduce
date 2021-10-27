# map-reduce
Trying to implement Map-Reduce on k8s

* Install charts from k8s-charts folder

  `helm install -n map map k8_chars --create-namespace`
  
* Should spin two masters and 4 worker replicas

* Master lifts the load of splitting workload into available number of reducers, while workers perform the reduce operation

* Workers run with Headless service, so ip of workers are fetch from master by dns lookup
