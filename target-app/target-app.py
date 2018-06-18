#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import sys
import random
import inspect


#from prometheus_client import start_http_server, Histogram, Gauge, Counter

from prometheus_client import start_http_server, Counter

req_counter = Counter("request_count", "Total number of requests")

counter_val = 0
step = 10
update_interval = 1
restart_interval = 300 
restart_time = 60

port = 8000
start_http_server(port)
print("Server listening at http://localhost:%s" % port)
print("Interval: %ds" % update_interval)

def reset(counter):
	with counter._value._lock:
		counter._value._value = 0.0

while True:
    counter_val = counter_val + step
    req_counter.inc(step)
    # simulate reset every X intervals
    if (counter_val > restart_interval * step):
    	counter_val = 0
    	reset(req_counter) 
    	time.sleep(restart_time)
    	print("service restarting...")
    else:
    	print(counter_val)
    	time.sleep(update_interval)