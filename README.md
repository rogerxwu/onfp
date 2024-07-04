# Network Flow at Scale (NFS)
[![Elastic Stack version](https://img.shields.io/badge/Elastic%20Stack-8.11.0-00bfb3?style=flat&logo=elastic-stack)](https://www.elastic.co/blog/category/releases)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This project is aim to provide a full stack sflow/netflow collecting and analysising solution that can be implemented at scale.


## System design
This solution leverages ELK stack to ingest/index/vistualize the netflow/sflow data. In order to deploy it at scale, you should consider to use L4 load balance services like Nginx or AVI to distribute the netflow/sflow traffic to multiple LogStash nodes. We will discuss how to further scale this solution at the section 'how to scale'
NetFlow and SFlow dataset to simulate 
![alt text](https://github.com/rogerxwu/nfs/blob/main/static/image.png)

### Installation
Install docker and docker-compose
```
cd nfs
docker-compose up --build
```

### Generate NetFlow/Sflow for testing
In order to verify the data accuratcy in elasticsearch, use the python script at scripts folder to generate traffic.
```
cd script
poetry install
poetry run python send_netflow_v5.py
poetry run python send_sflow_v5.py
```

## Demo
![alt text](https://github.com/rogerxwu/nfs/blob/main/static/flow.png)
## How SFlow pipeline works
https://blog.sflow.com/2011/12/sflowtool.html


## Monitoring
Without a monitoring on the platform, its hard to find the bottleneck or performance gap


CPU, Memory, Disk (Use node_exporter to send metrics to prometheus)
    - Elasticsearch Node
    - Grafana Node
    - Logstash Node
    - Nginx Node
    - Kibana Node
flow rate
    - from device to nginx (when generate the traffic, send the data to promethus)
    - from nginx to logstash (setup logging to promethus)
    - data received rate in elasticsearch (send to promethus)



## Optimization
The optimizaton on the system is the most trick part. Based on the traffic load, you need different design on ingest layer and backend cluster. Let's assume, we need 500k event/s ingested to the elasticsearch cluster. how to deisgn the logstash cluster and elasticsearch cluster?

For Logstash cluster, you should consider to enable 'persistent queue' to handle the back pressure, when traffic spiking, no data lost. However, if you persist the data you received, you need to make sure the emit rate equals or bigger than received rate, otherwise the data in the queue will drive your node down eventually. At this circumstance, you should conside the following optimzation
1. Send the traffic to coordinate nodes directly, only if you have coordinate nodes
2. Add more logstash nodes, load-balance the traffic
3. Edit the logstash.yml file to maxmize the utilization on hardware resource

For elasticsearch cluster, you need add more functional nodes to increase the capacity
1. more coordinate nodes
2. more ingest nodes
3. set the num_replica to 0 in template, but you should be aware of the shortcoming of setting it
5. bulk index 


## How to use k8s to auto scale logstash nodes based on usage