#!/bin/bash

(sudo docker stop prometheus || true) && (sudo docker rm prometheus || true) && sudo docker build -t prometheus prometheus
(sudo docker stop sample-client || true) && (sudo docker rm sample-client || true) && sudo docker build -t sample-client sample-client 