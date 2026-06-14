#!/bin/bash

######
# Создание индекса

INDEX_ES="favorite_films" 
TIME_TO_SLEEP=3


curl -XPUT http://localhost:9200/$INDEX_ES

sleep $TIME_TO_SLEEP

######
# Внесение данных с заранее внесенным индексом

# POST favorite_films/_doc/1
# {
#   "title": "Catch me If you can",
#   "type": "drama",
#   "year": 2001
# }
#

echo ''
echo 'ADD DATA WITH INDEX'
echo ''

curl -XPOST http://localhost:9200/$INDEX_ES/_doc/1 -H 'Content-Type: application/json' -d '{
  "title": "EuroTrip",
  "type": "camedy",
  "year": 2004
}'

sleep $TIME_TO_SLEEP

# Внесение данных
echo ''
echo 'ADD DATA WITHOUT INDEX'
echo ''

curl -XPOST http://localhost:9200/$INDEX_ES/_doc/ -H 'Content-Type: application/json' -d '{
  "title": "EuroTrip",
  "type": "camedy",
  "year": 2004
}'
sleep $TIME_TO_SLEEP


# Внесение большого количества данных
# необходим в корне файл info.json
echo ''
echo 'ADD DATA BULK'
echo ''

curl -H "Content-Type: application/x-ndjson" -XPOST "http://localhost:9200/$INDEX_ES/_bulk?pretty" --data-binary @info.json

#######
#### изменения данных

# Обновление данных (старые данные удаляет, поэтому переносить надо и поля)
echo ''
echo 'UPDATE DATA'
echo ''

curl -XPOST http://localhost:9200/$INDEX_ES/_doc/1 -H 'Content-Type: application/json' -d '{
  "title": "Catch me If you can",
  "type": "drama",
  "year": 2002
}'


sleep $TIME_TO_SLEEP

# Обновление данных без затирания (_doc  _update)
echo ''
echo 'UPDATE DATA'
echo ''

curl -XPOST http://localhost:9200/$INDEX_ES/_update/1 -H 'Content-Type: application/json' -d '{
  "doc": {
    "type": ["crime","drama"]
  }
}'

sleep $TIME_TO_SLEEP

####### GET DATA
#
# Получение всей информации

echo ''
echo 'GET DATA'
echo ''

curl -s -XGET http://localhost:9200/$INDEX_ES/_search/

sleep $TIME_TO_SLEEP

# Получение информации по id
echo ''
echo 'GET DATA BY ID'
echo ''
curl -s -XGET http://localhost:9200/$INDEX_ES/_doc/1


sleep $TIME_TO_SLEEP

# Поиск, где дата выхода фильма от 2002 до 2004  
echo ''
echo 'GET DATA BY WHERE (film create 2002 - 2004)'
echo ''

curl -s -XGET http://localhost:9200/$INDEX_ES/_search/ -H 'Content-Type: application/json' -d '{
  "query": {
    "range": {
      "year": {
        "gte": 2002,
        "lte": 2004
      }
    }
  }
}'

sleep $TIME_TO_SLEEP

# Получение всех фильмов, где жанр фильма комедия
echo ''
echo 'GET COMEDY'
echo ''

# GET favorite_films/_search
# {
#   "query": {
#     "match": {
#       "type":"camedy"
#     }
#   }
# }

curl -s -XGET http://localhost:9200/$INDEX_ES/_search/ -H 'Content-Type: application/json' -d '{
  "query": {
    "match": {
      "type":"camedy"
    }
  }
}'

sleep $TIME_TO_SLEEP

# При использовании нескольких слов происходит поиск по одному слову, не все вместе 
# Запросы одинаковы
echo ''
echo 'TWO WORD REQUEST'
echo ''

curl -s -XGET http://localhost:9200/$INDEX_ES/_search/ -H 'Content-Type: application/json' -d '{
  "query": {
    "match": {
      "type":"camedy drama"
    }
  }
}'

echo ''

curl -s -XGET http://localhost:9200/$INDEX_ES/_search/ -H 'Content-Type: application/json' -d '{
  "query": {
    "match": {
      "type":"drama camedy"
    }
  }
}'


sleep $TIME_TO_SLEEP

# Использование нескольких слов, поиск всех слов вместе
echo ''
echo 'SEARCH AND'
echo ''

curl -s -XGET http://localhost:9200/$INDEX_ES/_search/ -H 'Content-Type: application/json' -d '{
  "query": {
    "match": {
      "type": {
        "query": "drama camedy",
        "operator": "and"
      }
    }
  }
}'

sleep $TIME_TO_SLEEP

# Поиск фразы
echo ''
echo 'SEARCH PHRASE'
echo ''

curl -s -XGET http://localhost:9200/$INDEX_ES/_search/ -H 'Content-Type: application/json' -d '{
  "query": {
    "match_phrase": {
      "title": {
        "query": "The Hangover Part"
      }
    }
  }
}'

sleep $TIME_TO_SLEEP

# Поиск по множеству полей fields": ["title","type"]
echo ''
echo 'SEARCH BY SOME FIELDS'
echo ''

curl -s -XGET http://localhost:9200/$INDEX_ES/_search/ -H 'Content-Type: application/json' -d '{
  "query": {
    "multi_match": {
        "query": "The Hangover",
        "fields": ["title","type"],
        "type": "phrase"
      }
  }
}'

sleep $TIME_TO_SLEEP

# Поиск с обязательным содержанием фразы и определенного года
echo ''
echo 'MATCH PHRASE'
echo ''

curl -s -XGET http://localhost:9200/$INDEX_ES/_search/ -H 'Content-Type: application/json' -d '{
  "query": {
    "bool": {
      "must": [
        {
          "match_phrase": {
            "title": "The Hangover Part"
          }
        },
        {
          "match": {
            "year": 2013
          }
        }
      ]
    }
  }
}'


sleep $TIME_TO_SLEEP

# Поиск агрегатных значений по определённому названию
echo ''
echo ''
echo ''

curl -s -XGET http://localhost:9200/$INDEX_ES/_search/ -H 'Content-Type: application/json' -d '{
  "query": {
    "match_phrase": {
      "title": "The Hangover"
    }
  },
  "aggs": {
    "average_year": {
      "avg": {
        "field": "year"
      }
    }
  }
}'


