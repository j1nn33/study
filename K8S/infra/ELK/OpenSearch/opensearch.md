##### Описание 
##### установка на Virtual
##### установка в k8s
##### тестироване 


##### Описание 
```
  - ./ELK/arch.md
  - назначение нод
  - жизненый цикл данных
  - масштабирование 
  
```
##### установка на Virtual
```bash
##### INSTALL ELASTICSEARCH
# https://opendistro.github.io/for-elasticsearch-docs/docs/install/rpm/
# Create the repository file
sudo curl https://d3g5vo6xdbdb9a.cloudfront.net/yum/opendistroforelasticsearch-artifacts.repo -o /etc/yum.repos.d/opendistroforelasticsearch-artifacts.repo

yum install java-11-openjdk-devel 
yum install wget unzip curl mc

# List all available Open Distro versions
yum list opendistroforelasticsearch --showduplicates
yum install opendistroforelasticsearch-1.13.2

# start elasticsearch.service 
systemctl start elasticsearch.service

# Tets with SSL (by default config)
curl -XGET https://localhost:9200 -u 'admin:admin' --insecure
curl -XGET https://localhost:9200/_cat/nodes?v -u 'admin:admin' --insecure
curl -XGET https://localhost:9200/_cat/plugins?v -u 'admin:admin' --insecure
curl -XGET https://localhost:9200/_cluster/health?pretty -u 'admin:admin' --insecure

# Tets without SSL 
# /etc/elasticsearch/elasticsearch.yml
# #opendistro_security.ssl.http.enabled: true

curl -XGET http://localhost:9200 -u 'admin:admin'
curl -XGET http://localhost:9200/_cat/nodes?v -u 'admin:admin'
curl -XGET http://localhost:9200/_cat/plugins?v -u 'admin:admin'
curl -XGET http://localhost:9200/_cluster/health?pretty -u 'admin:admin'

##### INSTALL KIBANA
# https://opendistro.github.io/for-elasticsearch-docs/docs/kibana/

yum install opendistroforelasticsearch-kibana
/bin/systemctl enable kibana.service
/bin/systemctl daemon-reload
vim /etc/nginx/conf.d/kibana.conf

```
##### установка в k8s
```
Посмотреть можно здесь 
https://github.com/BigKAA/youtube/blob/master/opensearch/README.md
```
##### тестироване 
```bash

# создание патернов индексов 
kube*   time
host*   timestamp

GET _cat/indices/*
DELETE <index>



```