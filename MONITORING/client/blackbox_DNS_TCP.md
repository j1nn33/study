##### Настройка DNS

```
проверяем можем ли разрешить DNS ya.ru
```

```bash
cat <<EOF >> /etc/blackbox_exporter/blackbox.yml
  dns_slurm:
    prober: dns
    timeout: 2s
    dns:
      query_name: ya.ru
      preferred_ip_protocol: ip4
EOF



systemctl restart blackbox_exporter
```

```bash

# Проверка 

curl -is "http://localhost:9115/probe?module=dns_slurm&target=8.8.8.8" | grep probe_success

# # HELP probe_success Displays whether or not the probe was a success
# # TYPE probe_success gauge
# probe_success 1


# module - передаётся имя проверки,
# target – на какой DNS сервер будет отправлен запрос. 

```
```
timeout  
# Default: scrape_timeout
# Время, после которого проверка будет считаться неудачной. Если значение не
# задано, используется scrape_timeout, который передал Prometheus.

preferred_ip_protocol
# Default: ip6
# протокол используемый для проверки. Допустимые значения: ip4| ip6.

source_ip_address
# Default: -
# Если на сервере несколько IP адресов, можно указать, с какого ip будет проводиться проверка.

transport_protocol
# Default: udp
# Протокол, по которому будет производиться проверка. Возможные значения: udp, tcp.

query_name:
# Default: -
# Запрос, который будет отправлен на DNS сервер.

query_type
# Default: "ANY"
# Тип записи, который будет запрашиваться. По умолчанию, запрашиваются все типы записей.

```

##### TCP протокол

```
В данной конфигурации будет проверяться, присутствует ли в ответе строка: SSH-2.0-
```

```bash

cat <<EOF >> /etc/blackbox_exporter/blackbox.yml
  tcp_slurm:
    prober: tcp
    timeout: 2s
    tcp:
      query_response:
      - expect: "^SSH-2.0-"
      preferred_ip_protocol: ip4
EOF



systemctl restart blackbox_exporter
```

```bash

# Проверка 
curl -is "http://localhost:9115/probe?module=tcp_slurm&target=127.0.0.1:22" | grep probe_success

# # HELP probe_success Displays whether or not the probe was a success
# # TYPE probe_success gauge
# probe_success 1


# module -  имя проверки, 
# target – IP адрес хоста и порт, для которых будет выполнена проверка.
```

```
timeout
# Default: scrape_timeout
# Время, после которого проверка будет считаться неудачной.  
# Если значение не задано, используется scrape_timeout, который передал Prometheus.

preferred_ip_protocol
# Default: ip6
# протокол используемый для проверки. Допустимые значения: ip4| ip6.

query_response
#    expect   - проверка на наличие строки в ответе.
#    send     - позволяет задать, какой запрос будет отправлен на сервер.
#    starttls - задает, будет ли использоваться tls при подключении, по умолчанию – false.

source_ip_address
# Default: -
# Если на сервере несколько IP адресов, можно указать, с какого ip будет проводиться проверка.

tls
# Default: false
# Использовать ли tls после подключения.

tls_config
# Настройки для tls. Возможны следующие настройки для tls:
#    insecure_skip_verify – проверять ли валидность сертификата. Значение поумолчанию – false.
#    ca_file              – путь к файлу с корневыми сертификатами.
#    cert_file            – путь к файлу с клиентским сертификатом.
#    key_file             – путь к файлу с клиентским ключом.
#    server_name          – строка для проверки имени сервера.


```