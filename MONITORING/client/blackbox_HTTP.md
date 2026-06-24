##### HTTP протокол

```
проверка предназначена для проверки сервисов с использованием HTTP протокола
В данной конфигурации для проверки используется протокол ip v4, 
проверяется версия HTTP, код ответа, метод GET. 
проверка закончится с ошибкой, если не
                      используется https # или если в ответе отсутствует слово: Prometheus
```

```bash

cat <<EOF >> /etc/blackbox_exporter/blackbox.yml
  http_slurm:
    prober: http
    timeout: 2s
    http:
      preferred_ip_protocol: ip4
      valid_http_versions: ["HTTP/1.1", "HTTP/2"]
      valid_status_codes: [200]
      fail_if_not_ssl: true
      method: GET
      #fail_if_body_not_matches_regexp:
      #  - "Prometheus"
EOF


systemctl restart blackbox_exporter
```

```bash 


curl -is "http://localhost:9115/probe?module=http_slurm&target=https://ya.ru" | grep probe_success

# HELP probe_success Displays whether or not the probe was a success
# TYPE probe_success gauge
probe_success 0

curl -is "http://localhost:9115/probe?module=http_slurm&target=https://yandex.ru" | grep probe_success
# HELP probe_success Displays whether or not the probe was a success
# TYPE probe_success gauge
probe_success 1


# module - имя проверки
# target – адрес веб сайта, который проверяется. 
# Адрес сайта может передаваться вместе со схемой. Если схема не указана, то будет использоваться http.

```


```
timeout
# Default: scrape_timeout
# Время, после которого проверка будет считаться неудачной.
# Если значение не задано, используется scrape_timeout, который передал Prometheus.

preferred_ip_protocol
# Default: ip6
# Какой протокол используется для проверки. Допустимые значения: ip4| ip6.

source_ip_address
# Default: -
# Если на сервере несколько IP адресов, можно указать, с какого ip будет проводиться проверка.

valid_status_codes
# default: 200
# Проверка считается неудачной, если код не соответствует заданному.

valid_http_versions
# Проверка считается неудачной, если версия HTTP не соответствует строке.

method
# Default: GET
# Тип запроса. Возможные значения: GET | POST.

headers
# Список заголовков, которые передаются во время проверки.

no_follow_redirects
# Default: false
# Следовать ли редиректам при проверке.

fail_if_ssl
# Deafult: false
# Проверка считается неуспешной, если соединение установлено по https.

fail_if_body_matches_regexp
# Проверка считается неуспешной, если в body присутствует строка удовлетворяющая регулярному выражению.

fail_if_body_not_matches_regexp
# Проверка считается неуспешной, если в body отсутствует строка удовлетворяющая регулярному выражению.

fail_if_header_matches
# Проверка считается неуспешной, если в ответе присутствует заголовок, значение которого удовлетворяет регулярному выражению.
#      header        – имя заголовка, который проверяется.
#      regexp        – регулярное выражение, которое проверяется в значении заголовка.
#      allow_missing – разрешить отсутствие заголовка. По умолчанию: false.

fail_if_header_not_matches
# Проверка считается неуспешной, если в ответе отсутствует заголовок, значение которого удовлетворяет регулярному выражению.
#      header        – имя заголовка, который проверяется.
#      regexp        – регулярное выражение, которое проверяется в значении заголовка.
#      allow_missing – разрешить отсутствие заголовка. По умолчанию: false.

basic_auth
# username – имя пользователя, которое используется для авторизации на проверяемом сайте.
# password – пароль, который используется для авторизации на проверяемом сайте.

bearer_token
# Токен для bearer авторизации.

bearer_token_file
# Файл, который содержит токен для bearer авторизации. 

proxy_url
# Адрес proxy сервера, если проверку необходимо выполнить через proxy сервер.

body
# Body, которое передается вместе с запросом.

tls_config
#      insecure_skip_verify – проверять ли валидность сертификата. Значение по умолчанию: false
#      ca_file              – путь к файлу с корневыми сертификатами.
#      cert_file            – путь к файлу с клиентским сертификатом.
#      key_file             – путь к файлу с клиентским ключом.
#      server_name          – строка для проверки имени сервера.
```