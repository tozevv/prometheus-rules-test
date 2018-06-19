# Prometheus Rules Playground

## Overview

This projects runs a docker composer with a prometheus and a sample target test application. The target application creates the test metrics that are scrapped by the prometheus instance with recording rules support.
 
Both services start by running `docker-compose up` and stop by running `docker-compose down`. 

If you need to rebuild the apps or try a new configuraiton run `docker-compose build`.

Prometheus is available in  <http://localhost:9090/> and the application metrics in <http://localhost:8000/>.

## Data Aggregation Test

Prometheus rules can be leveraged to aggregate and summarize metrics data by creating new coarse grained metrics that are enable faster queries. This is particular useful for metrics that require data from long periods (> 1 day) like availability KPIs. 

The purpose of this test is to evaluate how changes in interval and rule format affect the recorded metrics by comparing them with the baseline value.

The test scenario has a single counter `request_count`. The target application increments `request_count` by `10` every second. Prometheus scrapes this rule every `15 seconds`. Every `5 minutes` the app restarts the counter, thus simulating a restart. This is important to test how the rules behave regarding counter monoticity. 

### Rules Tested 

For this test we used 2 different rule scrapping intervals (1m and 10m) and two different approaches each:

   - *Sample the counter*: The rules `request_count_total` just sample the aggregation of the counter at the moment of running. This is a simple sample of the counter and identicial to the example provided in Prometheus documentation for recording rules. Our concern with this approach is that it may fail considerably with counter resets.
   - *Counter delta*: The rules `request_count_increase` instead of sampling the counter compute the increase (delta) in the same period as the scraping interval. Counter resets are accounted for. However failed to record the rule will result in incorrect results. 

   
The following table includes 
   

```
groups:
- name: request_count_1m
  interval: 1m
  rules:
  - record: request_count_increase_1m
    expr: sum(increase(request_count[1m]))
  - record: request_count_total_1m
    expr: sum(request_count)
- name: request_count_10m
  interval: 10m
  rules:
  - record: request_count_increase_10m
    expr: sum(increase(request_count[10m]))
  - record: request_count_total_10m
    expr: sum(request_count)
```

## Results 

This is the baseline query we are trying to summarize:

```increase(request_count[1h])```

For our test the output was `29232` (rounded).

|name|rule|query|result|error|
|---|---|---|---:|---:|
|`request_count_total_1m`|`sum(request_count)`|`increase(request_count_total_1m[1h])`|	26705| -9% |
|`request_count_total_10m`|`sum(request_count)`|`increase(request_count_total_10m[1h])`|	81834| 180% |
|`request_count_increase_1m`|`sum(increase(request_count[1m]))`|`sum_over_time(request_count_increase_1m[1h])`|28298| -3% |
|`request_count_increase_10m`|`sum(increase(request_count[10m]))`|`sum_over_time(request_count_increase_10m[1h])`|29056| -1% |

As predicted sampling the counters doesn't work well with resets.

Prometheus was clearly not designed for this use case. However we feel that recording rules have advantages and we are willing to accept the risks as a temporary solution.

In the long term we should consider export the Prometheus time-series data into InfluxDB or other system to facilitate long-term data aggregation for statistic and time-series analysis.

For a short term solution the increase counters are the way to go.