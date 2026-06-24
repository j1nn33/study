#### Установка Blackbox Exporter

https://github.com/prometheus/blackbox_exporter/releases

```bash

cd /monitoring
wget https://github.com/prometheus/blackbox_exporter/releases/download/v0.27.0/blackbox_exporter-0.27.0.linux-amd64.tar.gz
tar -xvf blackbox_exporter-0.27.0.linux-amd64.tar.gz
cd blackbox_exporter-0.27.0.linux-amd64
mv blackbox_exporter /usr/local/bin/
```
```
Создаем каталог для конфигурационных файлов и копируем конфигурационные файл по умолчанию.
```

```bash
mkdir /etc/blackbox_exporter
cp blackbox.yml /etc/blackbox_exporter/
```
```
список параметров вынесен в файл: /etc/sysconfig/blackbox_exporter

- переопределяем конфиг по умолчанию (blackbox exporter ищет его в том же каталоге где и бинарный файл)

требует root привилеги
EnvironmentFile все переменные из файла, указанного в этой директиве, добавляются в env 

```
```bash
cat <<EOF > /etc/sysconfig/blackbox_exporter
OPTIONS="--config.file=/etc/blackbox_exporter/blackbox.yml"
EOF
```

```
созданиие systemd 
```
```bash
vim /usr/lib/systemd/system/blackbox_exporter.service
[Unit]
Description=Prometheus exporter for machine metrics
Documentation=https://github.com/prometheus/blackbox_exporter
After=network.target

[Service]
Restart=always
User=root
EnvironmentFile=/etc/sysconfig/blackbox_exporter
ExecStart=/usr/local/bin/blackbox_exporter ${OPTIONS}
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target


```
```


```

```bash
systemctl daemon-reload
systemctl start blackbox_exporter
systemctl enable blackbox_exporter
```
```
при проблемах на старте проверить 
tail -f /var/log/messges
# blackbox_exporter.service: Failed to execute command: Permission denied
# systemd[4889]: blackbox_exporter.service: Failed at step EXEC spawning /usr/local/bin/blackbox_exporter: Permission denied
# systemd[1]: blackbox_exporter.service: Main process exited, code=exited, status=203/EXEC
```
```bash
getenforce
setenforce 0
systemctl start blackbox_exporter

# запустить бинарник вручную от root: 
/usr/local/bin/blackbox_exporter --config.file=/etc/blackbox_exporter/blackbox.yml
```

```bash 
curl -I http://localhost:9115
# HTTP/1.1 200 OK
# Content-Type: text/html
# Date: Tue, 04 Aug 2026 17:47:40 GMT
# Content-Length: 544


http://192.168.1.236:9115/
```


###### Особенности использования Blackbox Exporter
```

1. По умолчанию, все проверки выполняются по IPv6. Рекомендуется изменить значение
на IPv4. Для этого надо использовать директиву: preferred_ip_protocol: ip4 в настройках
каждого модуля.
2. По ссылке /metrics Blackbox Exporter отдает данные о своей работе, такие как:
потребление cpu, потребление ram и т.д. Результаты проверки доступны по url /probe.
3. Для получения подробностей по проверке в параметры запроса нужно добавить:
debug=true


```