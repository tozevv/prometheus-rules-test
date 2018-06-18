#!/bin/bash
#!/bin/bash

docker network create prom-rules-net

(sudo docker stop prom-rules-server || true) && sudo docker run --name prom-rules-server --net prom-rules-net -p 9090:9090 -v prom-data:/prometheus prometheus
(sudo docker stop prom-rules-app || true) && sudo docker run --name prom-rules-app --net prom-rules-net -p 8000:8000 test-app