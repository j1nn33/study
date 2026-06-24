### Установка Prometheus

```
https://github.com/prometheus/prometheus/releases
```

```bash

# Создаем пользователя Prometheus:
useradd prometheus --comment "Prometheus server user" --shell /bin/false

cat cat /etc/passwd | grep prometheus
# prometheus:x:1000:1000:Prometheus server user:/home/prometheus:/bin/false

wget https://github.com/prometheus/prometheus/releases/download/v3.13.1/prometheus-3.13.1.linux-386.tar.gz
tar -xvf prometheus-3.13.1.linux-386.tar.gz
cd prometheus-3.13.1.linux-386
mv prometheus /usr/local/bin/

# Создаем каталог для конфигурационных файлов, копируем конфигурационные файлы
# по умолчанию и выставляем на них права:
mkdir /etc/prometheus
cp prometheus.yml /etc/prometheus/
chown -R prometheus:prometheus /etc/prometheus

# Создаем каталог для Prometheus DB и выставляем на него права:
mkdir /var/lib/prometheus
chown prometheus:prometheus /var/lib/prometheus



# Создадим файл со списком ключей для запуска Prometheus.
# Для того, чтобы каждый раз не перечитывать настройки systemd, список ключей вынесен в файл: /etc/sysconfig/prometheus
# Prometheus имеет конфигурационный файл и, по умолчанию, ищет его в том же каталоге, 
# где и бинарный файл, то через ключ --config.file задаем путь до конфигурационного файла.
# с помощью ключа: --storage.tsdb.path задаем путь до каталога, где будет располагаться Prometheus DB

cat <<EOF > /etc/sysconfig/prometheus
OPTIONS="--config.file=/etc/prometheus/prometheus.yml \
--storage.tsdb.path=/var/lib/prometheus/"
EOF

# Создаем systemd сервис:

vim /usr/lib/systemd/system/prometheus.service
```
```
[Unit]
Description=Prometheus Server
Documentation=https://github.com/prometheus/prometheus
After=network.target

[Service]
Restart=always
User=prometheus
Group=prometheus
#EnvironmentFile=/etc/sysconfig/prometheus
#ExecStart=/usr/local/bin/prometheus ${OPTIONS}
ExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/var/lib/prometheus/

ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s


[Install]
WantedBy=multi-user.target

```
```bash
systemctl daemon-reload
systemctl restart prometeus.service
systemctl enable prometheus


# Проверяем работу
curl -XGET -IL http://localhost:9090/graph

# HTTP/1.1 200 OK
# Date: Sat, 08 Aug 2026 14:26:39 GMT
# Content-Length: 1752
# Content-Type: text/html; charset=utf-8


http://192.168.1.236:9090/query?

```


#### Проверка конфигурационного файла.


```bash 
# утилита для тестирования конфигурационных файлов.

cp promtool /usr/local/bin/
# Для проверки конфигурационного файла запускаем команду:

promtool check config /etc/prometheus/prometheus.yml
# Checking /etc/prometheus/prometheus.yml
#  SUCCESS: /etc/prometheus/prometheus.yml is valid prometheus config file syntax


```

#### Основной конфигурационный файл Prometheus

```
prometheus_yml.md  
```

#### Ключи запуска Prometheus

```bash

--config.file
Default: "prometheus.yml"
# Путь к конфигурационному файлу Prometheus. Если путь не полный, то поиск
# производится по каталогу, из которого запущен Prometheus.

--web.listen-address
Default: "0.0.0.0:9090"
# Адрес и порт, по которому доступны UI и метрики Prometheus.

--web.read-timeout
Default: 5m
# Максимальное время ожидания ответа от сервера и закрытия idle подключений.

--storage.tsdb.path
Default: "data/"
# Путь к каталогу для сохранения метрик.

--storage.tsdb.retention.time
Default: -
# Как долго хранить данные метрик. Время хранения метрик, по умолчанию: 15 дней.

--storage.tsdb.retention.size
Default: 0B
# Максимальный размер, отведенный под хранение метрик.
# Допускаются следующие единицы: KB, MB, GB, TB, PB. Первыми удаляются наиболее старые данные.

--storage.remote.flush-deadline
Default: 1m
# Как долго ожидать окончания процесса сохранения данных при restart и reload.

--rules.alert.for-outage-tolerance
Default: 1h
# Максимальное задержки для "for".

--rules.alert.for-grace-period
Default: 10m
# Минимальное время восстановления состояния.

--rules.alert.resend-delay
Default: 1m
# Минимальное время ожидания до отправки сообщения в Alertmanager.

--alertmanager.notification-queue-capacity
Default: 10000
# Максимальное число сообщений, ожидающих отправки в Alertmanager.
--alertmanager.timeout
Default: 10s

# Timeout для отправки сообщений в Alertmanager.
--query.timeout
Default: 2m

# Максимальное время для выполнения запроса, после этого запрос будет сброшен.

--query.max-concurrency
Default: 20
# Максимальное число параллельно выполняющихся запросов.

--log.level
Default: info
# Данный ключ устанавливает уровень логирования. Возможные уровни логирования:
# debug, info, warn, error.

--log.format
Defult: logfmt

# Данный ключ устанавливает формат логов. Доступные форматы: logfmt и json.

# Полный список ключей можно просмотреть с помощью команды help:
prometheus --help


```