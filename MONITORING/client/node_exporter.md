#### NODE EXPORTER

###### IMSTALL

https://github.com/prometheus/node_exporter/releases

```bash
mkdir monitoring
cd monitoring

wget https://github.com/prometheus/node_exporter/releases/download/v1.1xporter-1.12.1.linux-amd64.tar.gz
tar -xvf node_exporter-1.12.1.linux-amd64.tar.gz
cd node_exporter-1.12.1.linux-amd64
mv node_exporter /usr/local/bin/

```
```
Node Exporter не имеет конфигурационного файла и настраивается дополнительными ключами. 
Для того, чтобы каждый раз не перечитывать настройки systemd, список ключей вынесен в файл: 
/etc/sysconfig/node_exporte
```
```bash
cat <<EOF > /etc/sysconfig/node_exporter
OPTIONS=""
EOF

```
```
Node Exporter требует root привилеги

EnvironmentFile все переменные из файла, указанного в этой директиве, добавляются в env 

```
```bash

vim /usr/lib/systemd/system/node_exporter.service
# не стартует если OPTIONS нет 
```
```
[Unit]
Description=Prometheus Node exporter for machine metrics
Documentation=https://github.com/prometheus/node_exporter
After=network.target

[Service]
Restart=always
User=root
EnvironmentFile=/etc/sysconfig/node_exporter
ExecStart=/usr/local/bin/node_exporter ${OPTIONS}
#ExecStart=/usr/local/bin/node_exporter

Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target


```

```bash
systemctl daemon-reload
systemctl start node_exporter
systemctl enable node_exporter


curl -I http://localhost:9100
# HTTP/1.1 200 OK
# Content-Type: text/html; charset=UTF-8
# Date: Mon, 03 Aug 2026 17:50:51 GMT
# Content-Length: 1490

http://192.168.1.236:9100/metrics


```

```bash 
# Ключи запуска Node Exporter
# Далее приведен список наиболее востребованных ключей Node Exporter
--log.level
# Default: info
# Данный ключ устанавливает уровень логирования. Возможные уровни логирования:
# debug, info, warn, error.
--log.format
# Defult: logfmt
# Данный ключ устанавливает формат логов. Доступные форматы: logfmt и json.
--web.listen-address
# Default: ":9100"
# Данный ключ устанавливает адрес и порт, по которому будет доступен Node Exporter.
--web.telemetry-path
# Default: "/metrics"
# Данный ключ устанавливает адрес, по которому доступны результаты экспозиции.
--web.disable-exporter-metrics
Default: -
# Данный ключ устанавливает список метрик, которые будут исключены из экспозиции.
# Например, для исключения всех метрик, имя которых начинается с go_, значение ключа
# будет: go_*. Допускается использовать перечисление нескольких метрик, с запятой в
# качестве разделителя.
# Полный список ключей можно просмотреть с помощью команды help.
node_exporter --help
```


