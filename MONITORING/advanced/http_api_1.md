##### Общие сведения для запросов API
```
- Запросы мгновенного вектора
- Запрос вектора за период времени
- Поиск временных рядов на основании labels
- Получение списка меток
- Запрос значений для label

```

###### Запросы мгновенного вектора
```
Ednpoint: /api/v1/query
Method:   GET | POST

Параметры запроса:
          query   – строка запроса PromQL.
          time    – временная метка, за которую надо выбрать данные. Если параметр не задан, берется текущее время сервера.
          timeout – максимальное время выполнения запроса. Параметр не является
                    обязательным. Если параметр не задан, используется значение query.timeout.

```

```bash

http://192.168.1.236:9090/api/v1/query?query=up&

curl 'http://localhost:9090/api/v1/query?query=up&time=2026-08-15T09:10:51.781Z' | jq

```

```bash

curl -XPOST -H 'Content-Type: application/x-www-form-urlencoded' -d "query=up" -d "time=2026-08-15T09:10:51.781Z" http://localhost:9090/api/v1/query

# Content-Type используется: application/x-www-form-urlencoded.

```


###### Запрос вектора за период времени
```
Ednpoint: /api/v1/query_range
Method:   GET | POST

Параметры запроса:
          query   – строка запроса PromQL.
          start   – временная метка начала вектора.
          end     – временная метка окончания вектора.
          step    – шаг выборки данных; допустимый формат [0-9]+[smhdwy], например 5s, либо число float(секунды).
          timeout – максимальное время выполнения запроса. Необязательный
                    параметр. Если параметр не задан, используется значение query.timeout.


Пример. 
Запрос: up, за период с 15.08.2026 09:10.51 по 15.08.2026 09:10.51, с шагом в 30 секунд:
```

```bash
curl 'http://localhost:9090/api/v1/query_range?query=up&start=2026-08-15T09:10:51.781Z&end=2026-08-15T09:15:51.781Z&step=30s' | jq


```

###### Поиск временных рядов на основании labels

```
Ednpoint: /api/v1/series
Method:   GET | POST

Параметры запроса:
          match[] – задает список меток, соответствие которым учитывается при
                    поиске. Необходимо задать хотя бы одно условие.
          start   – временная метка начала вектора.
          end     – временная метка окончания вектора.

Пример. 
В результате выполнения запроса мы получим данные по всем времяным
рядам, которые имеют имя node_disk_write_time_seconds_total и label device со значением sda
```

```bash

curl -XPOST -H 'Content-Type: application/x-www-form-urlencoded' -d 'match[]=node_disk_write_time_seconds_total{device="sda"}' http://localhost:9090/api/v1/series | jq
```
###### Получение списка меток

```
Endpoint: /api/v1/labels
Method:   GET | POST

Параметры запроса: -

Данный запрос позволяет получить список всех labels.

```
```bash 
curl 'http://localhost:9090/api/v1/labels' | jq

```
###### Запрос значений для label

```
Endpoint: /api/v1/labels
Method:   GET

Параметры запроса: -

Данный endpoint позволяет получить все значения для определенного label. 
Синтаксис запроса: /api/v1/labels/<label name>/values. 
Где <label name> это имя label, для которого необходимо получить значения.
```
```bash
curl 'http://localhost:9090/api/v1/label/instance/values' | jq

```

