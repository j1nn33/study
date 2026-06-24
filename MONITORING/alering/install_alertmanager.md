###### Установка Aletrmanager

```
https://github.com/prometheus/alertmanager/releases
```


```bash

# Создаем пользователя alertmanager
adduser --comment "User to run Alertmanager" --shell /bin/false alertmanager

cat /etc/passwd | grep alert
# alertmanager:x:1002:1002:User to run Alertmanager:/home/alertmanager:/bin/false

wget https://github.com/prometheus/alertmanager/releases/download/v0.32.2/alertmanager-0.32.2.linux-amd64.tar.gz
tar -xvf alertmanager-0.32.2.linux-amd64.tar.gz
cd alertmanager-0.32.2.linux-amd64
mv alertmanager /usr/local/bin

# Создаем каталог для конфигурационных файлов, копируем конфигурационные файлы по умолчанию и выставляем на них права

mkdir /etc/alertmanager
cp alertmanager.yml /etc/alertmanager/alertmanager.yml
chown alertmanager:alertmanager -R /etc/alertmanager

# Создаем каталог для хранения данных и выставляем на него права:

mkdir /var/lib/alertmanager/
chown alertmanager:alertmanager /var/lib/alertmanager/

# Создаем systemd сервис

vim /usr/lib/systemd/system/alertmanager.service
```

```
[Unit]
Description=Prometheus Alertmanager
Documentation=https://github.com/alertmanager/alertmanager
After=network.target

[Service]
User=alertmanager
Group=alertmanager
Restart=always
# EnvironmentFile=/etc/sysconfig/alertmanager
ExecStart=/usr/local/bin/alertmanager --config.file=/etc/alertmanager/alertmanager.yml --storage.path=/var/lib/alertmanager/


ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target

```

```bash

systemctl daemon-reload
systemctl start alertmanager.service
systemctl enable alertmanager.service

# Проверяем работу

curl -LI -XGET http://localhost:9093
# HTTP/1.1 200 OK
# Accept-Ranges: bytes
# Cache-Control: no-cache, no-store, must-revalidate
# Content-Length: 506
# Content-Type: text/html; charset=utf-8
# Expires: 0
# Pragma: no-cache
# Vary: Accept-Encoding
# Date: Fri, 14 Aug 2026 20:26:19 GMT


http://192.168.1.236:9093


# Добавляем отправку alert из Prometheus в Alertmanager.
# Для этого добавим targets в конфигурационный файл Prometheus:
# секция alerting уже имеется в конфигурационном файле. Необходимо ее привести к виду:

vim /etc/prometheus/prometheus.yml

```

```yaml
alerting:
  alertmanagers:
    - static_configs:
      - targets:
        - localhost:9093

```

```bash
# Проверяем корректность внесенных изменений
promtool check config /etc/prometheus/prometheus.yml

systemctl reload prometheus.service
```

###### Ключи запуска Alertmanager

```

--config.file
# Default: alertmanager.yml
# Имя конфигурационного файла.

--storage.path
# Default: data/
# Путь, куда сохраняются данные.

--data.retention
# Default: 120h
# Как долго хранить данные.

--web.listen-address
# Default: ":9093"
# Адрес и порт, по которому доступны UI и метрики Alertmanager.

--cluster.listen-address
# Default: "0.0.0.0:9094"
# Адрес для HA кластера. Пустое значение для отключения HA mode.

--cluster.advertise-address
# Default: -
# IP для анонса в кластере.

--cluster.peer
# Defalut: -
# Адреса peer в HA кластере.

--log.level
# Default: info
# уровень логирования. debug, info, warn, error.

--log.format
# Default: logfmt
#  формат логов. Доступные форматы: logfmt и json.

# Полный список ключей можно просмотреть с помощью команды help:
alertmanager --help


```