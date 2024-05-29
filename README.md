# Network Flow at Scale (NFaS)
[![Elastic Stack version](https://img.shields.io/badge/Elastic%20Stack-8.11.0-00bfb3?style=flat&logo=elastic-stack)](https://www.elastic.co/blog/category/releases)
[![Python]]
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This project is aim to provide a full stack sflow/netflow collecting and analysising solution that can be implemented at scale.


## System design
This solution leverages ELK stack to ingest/index/vistualize the netflow/sflow data. In order to deploy it at scale, you should consider to use L4 load balance services like Nginx or AVI to distribute the netflow/sflow traffic to multiple LogStash nodes. We will discuss how to further scale this solution at the section 'how to scale'
NetFlow and SFlow dataset to simulate 
![alt text](https://github.com/rogerxwu/nfs/blob/main/image.png)

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
![alt text](https://github.com/rogerxwu/nfs/blob/main/flow.png)
## How SFlow pipeline works
https://blog.sflow.com/2011/12/sflowtool.html

## How to scale

## Next
Deploy this solution in K8S env