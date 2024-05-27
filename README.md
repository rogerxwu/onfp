# Network Flow at Scale (NFaS)
This project is aim to provide a full stack sflow/netflow collection and analysis solution that can be implemented at scale.

[![Elastic Stack version](https://img.shields.io/badge/Elastic%20Stack-8.11.0-00bfb3?style=flat&logo=elastic-stack)](https://www.elastic.co/blog/category/releases)

## System design
Kibana
Elasticsearch or Opensearch
Logstash
NetFlow and SFlow dataset to simulate 

## Build the flow generator for test
In order to verify the data accuratcy in elasticsearch, we build a pcap file that include NetFlow V9 and SFlow data to ingest.

## Demo
Run docker-compose.yaml to turn the lab on
```
cd nfs
docker-compose up -d
```
Use scapy to generate netflow traffic

## How to scale

## Next
I will deploy this solution in K8S env