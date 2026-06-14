#!/bin/bash
# Создание индекса

echo ''
echo 'CREATE INDEX'
echo ''

curl -XPUT http://127.0.0.1:9200/table4 -H 'Content-Type: application/json' -d '{
"mappings": {
"properties": {
"text_field": {"type": "keyword"},
"number": {"type": "long"}
        }
    }
}'

sleep 3
# задержка по времни нужна чтобы изменинея залетели
# добавить документ
echo ''
echo 'ADD DATA '
echo ''



curl -XPOST http://127.0.0.1:9200/table4/_doc/ -H 'Content-Type: application/json' -d '{
"text_field": "my pretty text",
"number": 15
}' 

sleep 3


# обновить документ 
# curl -s -XGET "http://localhost:9200/table1/_search/" |  jq -r .hits.hits[0]._id
IDDOC=$(curl -s -XGET "http://localhost:9200/table4/_search/" |  jq -r .hits.hits[0]._id)

echo ''
echo 'UPDATE DATA'
echo ''
echo $IDDOC

sleep 3
curl -XPOST http://127.0.0.1:9200/table4/_doc/$IDDOC -H 'Content-Type: application/json' -d '{
"text_field": "my pretty text",
"number": 18
}'


curl -XPOST http://127.0.0.1:9200/$IDDOC/_doc/ -H 'Content-Type: application/
json' -d '{
    "text_field": "my pretty text",
    "number": 15
}'
curl -XPOST http://127.0.0.1:9200/$IDDOC/_doc/ -H 'Content-Type: application/
json' -d '{
    "text_field": "my code is perfect",
    "number": 16
}' 