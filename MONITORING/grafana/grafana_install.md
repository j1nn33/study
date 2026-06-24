###### Установка Grafana

```
# Документация 
https://grafana.com/docs/grafana/latest/setup-grafana/installation/redhat-rhel-fedora/

# Пакет 
https://dl.grafana.com/grafana/release/13.1.3/grafana_13.1.3_31135815010_linux_amd64.rpm
```

```bash

sudo useradd -r -s /bin/false grafana

cat /etc/passwd | grep grafana
# grafana:x:991:991:Grafana user account:/usr/share/grafana:/sbin/nologin

dnf install grafana_13.1.3_31135815010_linux_amd64.rpm

systemctl start grafana-server.service
systemctl status grafana-server.service


#  Проверяем работу

curl -IL http://localhost:3000/login

# HTTP/1.1 200 OK

http://192.168.1.236:3000/
```

###### Настройка Datasource
```
# Имя пользователя и пароль по умолчанию admin/admin

# Добавляем Prometheus в качеств

Name            – имя data source, должно быть уникальным.
URL             – адрес, где располагается prometheus.  http://localhost:9090
Access          – способ подключения к Prometheus. 
                  Server – запрос из браузера отправляется в grafana, grafana производит подключения к Prometheus. 
                  Browser – в этом случае запросы в Prometheus отправляются напрямую из браузера. 
                  Метод Browser менее предпочтителен, так как приводит к необходимости открывать прямой доступ к Prometheus.
Auth            – задаются учетные данные для подключения к Prom.
Scrape interval – рекомендуется выставить равным глобальному значению scrape,
                  установленному в Prometheus.
Query timeout   – задает максимальное время выполнения запроса к Prometheus.
HTTP Method     – метод для отправки запросов в Prometheus. Post запросы возможны, начиная с версии: 2.1.0

```

###### Настройка dashboard
```

Прмиер запроса, который будет использоваться для выборки данных:
rate(prometheus_http_requests_total{job="prometheus"}[5m])


```