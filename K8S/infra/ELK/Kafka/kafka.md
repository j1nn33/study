##### Описание 
##### установка на Virtual
##### тестироване 
##### установка Kafdrop
##### Работа c kafka

##### Описание 
```
https://kafka.apache.org/quickstart
https://kafka.apache.org/downloads


```
##### установка на Virtual
```bash
yum install java-11-openjdk-devel
wget https://dlcdn.apache.org/kafka/3.9.0/kafka_2.12-3.9.0.tgz

mkdir /opt/kafka
tar zxf kafka_*.tgz -C /opt/kafka --strip 1

# Добавим строку - данная директива разрешает ручное удаление темы из кафки.
vi /opt/kafka/config/server.properties

listeners=PLAINTEXT://<IP>:9092
delete.topic.enable = true

useradd -r -c 'Kafka broker user service' kafka
chown -R kafka:kafka /opt/kafka

# Создание systemd
vi /etc/systemd/system/zookeeper.service
# ---
[Unit]
Description=Zookeeper Service
Requires=network.target remote-fs.target
After=network.target remote-fs.target

[Service]
Type=simple
User=kafka
ExecStart=/opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
ExecStop=/opt/kafka/bin/zookeeper-server-stop.sh
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
# ---

vi /etc/systemd/system/kafka.service
# ---
[Unit]
Description=Kafka Service
Requires=zookeeper.service
After=zookeeper.service

[Service]
Type=simple
User=kafka
ExecStart=/bin/sh -c '/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties > /opt/kafka/kafka.log 2>&1'
ExecStop=/opt/kafka/bin/kafka-server-stop.sh
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
# ---

systemctl daemon-reload
# Разрешаем автозапуск сервисов zookeeper и kafka:
systemctl enable zookeeper kafka
systemctl start kafka
```

##### тестироване 
```bash 
# Проверить, что нужный нам сервис запустился и работаешь на порту 9092:
ss -tunlp | grep :9092

/opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server $(hostname -f):9092
/opt/kafka/bin/kafka-topics.sh --bootstrap-server $(hostname -f):9092 --list
```

##### установка Kafdrop
```bash
# Kafdrop – Kafka Web UI  
# https://github.com/obsidiandynamics/kafdrop

docker run -d --rm -p 9000:9000 \
    -e KAFKA_BROKERCONNECT=192.168.1.250:9092 \
    -e JVM_OPTS="-Xms128M -Xmx128M" \
    -e SERVER_SERVLET_CONTEXTPATH="/" \
    obsidiandynamics/kafdrop:3.31.0

# Доступ 
http://<IP>:9000/

docker зы
docker rm <name_pod> --force

```

###### Работа c kafka
```bash
# Создаем два топика 
#    - kube   - все логи связанные с k8s
#    - host   - все логи системного приложения сервера linux

/opt/kafka/bin/kafka-topics.sh --create --topic kube --bootstrap-server 192.168.1.250:9092
/opt/kafka/bin/kafka-topics.sh --create --topic host --bootstrap-server 192.168.1.250:9092

# Посмотреть сообщения 
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 192.168.1.250:9092 --topic host --from-beginning
/opt/kafka/bin/kafka-console-producer.sh --topic kube --bootstrap-server 192.168.1.250:9092


# Посмотреть сообщения с техническими полями 
./K8S/infra/ELK/image/kafka_message.png
# данные тех поля необходимо отфильтровать в vector

#     Offset     - information about the offset, as well as key and value length
#     Key        - key data
#     Value      - value data
#     Timestamp  - when the message was added
#     Headers    - header data

/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --partition 0 --offset 0 --property print.key=true --property print.timestamp=true
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 192.168.1.250:9092 --topic host --partition 0 --offset 0 --property print.key=true --property print.timestamp=true

# CreateTime:1736065276421        null    {"@timestamp":1736065275.0,"message":"Jan  5 11:21:15 control1 systemd[1]: run-containerd-runc-k8s.io-c6788661506244c8f5d09c581a795de1c38882588b1d5673e7f1fdb29445c9f2-runc.sSrG7I.mount: Succeeded.","host":"control1","app":"syslog","file":"/var/log/messages"}


```