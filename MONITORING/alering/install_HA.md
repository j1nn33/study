###### Настройка Alertmanager HA

```bash
# На втором серевре устанавливаем Aletrmanager по install_alertmanager.md

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
ExecStart=/usr/local/bin/alertmanager --config.file=/etc/alertmanager/alertmanager.yml --storage.path=/var/lib/alertmanager/ --cluster.peer <server1 monitoring IP>:9094


ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target

```

```
9094 - порт используется для обмена данными по протоколу gossip

На первом сервере также пропиываем 

--config.file=/etc/alertmanager/alertmanager.yml
--storage.path=/var/lib/alertmanager/ --cluster.peer <server2 monitoring IP>:9094

```

```bash
http://192.168.1.236:9093/#/status

http://192.168.1.237:9093/#/status
# Peers:
# Name: 01M00Z76P4VFB3ZQY0CJ9PERWF
# Address: 192.168.1.236:9094

# Name: 01M00Z76P4VFB3ZQY0CTCVEFG
# Address: 192.168.1.237:9094
```