##### API для получения конфигурации

```bash

# Конфигурация сервера
curl 'http://localhost:9090/api/v1/status/config' 

# Список ключей запуска
curl 'http://localhost:9090/api/v1/status/flags'

# Список targets
curl 'http://localhost:9090/api/v1/targets'
```

##### Rules и Alerts API

###### Alertmanagers

```bash
# список всех настроенных alertmanagers и их статус

curl 'http://localhost:9090/api/v1/alertmanagers' | jq

```
###### Alerts

```bash
#  список активных алертов

curl http://localhost:9090/api/v1/alerts | jq
```

###### Rules

```bash
# список всех правил: как record rules, так и alert rules

curl http://localhost:9090/api/v1/rules | jq
```

###### 

```bash
#  
```

###### 

```bash
#  
```

###### 

```bash
#  
```
