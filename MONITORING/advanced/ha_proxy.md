###### Настройка HA Proxy

```
Данная конфигурация позволяет проксировать запросы c 80 порта на один из Prometheus серверов.

```

```bash

# Устанавливаем HAProxy:
yum install -y haproxy

#  Настраиваем HAProxy.
# необходимо заменить <server1_IP> и <server2_IP> на реальные IP серверов:

vim /etc/haproxy/haproxy.cfg
```
```
#HA Proxy Config
global
    daemon
    maxconn 256

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    listen stats
    bind *:9999
    stats enable
    stats hide-version
    stats uri /stats
    stats auth admin:admin@123

frontend prometheus
    bind *:80
    use_backend prometheus

backend prometheus
    server prometheus1 <server1_IP>:9090 check
    server prometheus2 <server2_IP>:9090 check backup

```
```bash

# Запускаем HAProxy
systemctl start haproxy.service

curl -I http://localhost:80


```

```
Добавляем новый data source. 
В качестве URL указываем: http://localhost:80. 
В качестве Name указываем: Prometheus HA


Проверка результатов работы.
Для проверки необходимо выключить Prometheus поочередно на server1 и server2 и
убедиться, что графики продолжают отображаться
```