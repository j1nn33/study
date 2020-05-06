#!/bin/bash
curl -XPOST 'http://localhost:9200/app-test/data?pretty ' -H 'Content-Type: application/json'  -d'
{
   "name":"test-user",
   "age":30,
   "employee":"test-elastic"
}'
