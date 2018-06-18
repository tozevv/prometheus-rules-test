# Local Prometheus

## Instructions

```
(sudo docker stop prometheus || true) && (sudo docker rm prometheus || true) && sudo docker build -t prometheus . && sudo docker run --name prometheus -p 9090:9090 -v prom-data:/prometheus prometheus
```

This will stop prometheus if already running, build it and run it.

Prometheus will be listening at `http://localhost:9090`.

